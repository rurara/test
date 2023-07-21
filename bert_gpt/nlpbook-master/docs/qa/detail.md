---
layout: default
title: ↗️ Customization
parent: Question Answering
nav_order: 4
---


# ↗️ 나만의 질의 응답 모델 만들기
{: .no_toc }

커스텀 데이터, 토크나이저, 모델, 트레이너(trainer)로 나만의 질의 응답 모델을 만드는 과정을 소개합니다.
{: .fs-4 .ls-1 .code-example }

## Table of contents
{: .no_toc .text-delta .mt-6}

1. TOC
{:toc}

---

## 피처 구축 방식 이해하기

질의 응답 데이터는 그 포맷이 저마다 천차만별입니다. 데이터 포맷이 달라질 경우 우리 책에서 제공하는 질의 응답 튜토리얼 코드를 그대로 사용하기 어렵습니다. 이에 이 글에서는 우리 책에서 제공하는 코드의 피처 구축 방식을 이해하는 데 중점을 두도록 하겠습니다. 우리 책 질의 응답 튜토리얼의 피처 구축 관련 코드는 코드1과 같습니다.

## **코드1** 질의 응답 데이터 로딩 및 전처리
{: .no_toc .text-delta }

```python
# 데이터 로딩
from ratsnlp.nlpbook.qa import KorQuADV1Corpus
corpus = KorQuADV1Corpus(args)

# 데이터 전처리
from ratsnlp.nlpbook.qa import QADataset
train_dataset = QADataset(
	args=args,
	corpus=corpus,
	tokenizer=tokenizer,
	mode="train",
)
```

우리 책 튜토리얼의 학습데이터는 [KorQuAD 1.0](https://korquad.github.io/KorQuad%201.0/)입니다. 그 포맷은 `json`입니다. 코드2의 `KorQuADV1Corpus` 클래스는 위의 데이터 형식을 `QAExample`로 읽어들이는 역할을 합니다. 이와 관련해서는 [7-2장 Training](https://ratsgo.github.io/nlpbook/docs/qa/train)을 참고하시면 좋을 것 같습니다.


## **코드2** KorQuADV1Corpus
{: .no_toc .text-delta }

```python
import json

class KorQuADV1Corpus(QACorpus):

    def __init__(self):
        super().__init__()
        self.train_file = "KorQuAD_v1.0_train.json"
        self.val_file = "KorQuAD_v1.0_dev.json"

    def get_examples(self, corpus_dir, mode):
        examples = []
        if mode == "train":
            corpus_fpath = os.path.join(corpus_dir, self.train_file)
        elif mode == "val":
            corpus_fpath = os.path.join(corpus_dir, self.val_file)
        else:
            raise KeyError(f"mode({mode}) is not a valid split name")
        json_data = json.load(open(corpus_fpath, "r", encoding="utf-8"))["data"]
        for entry in tqdm(json_data):
            for paragraph in entry["paragraphs"]:
                context_text = paragraph["context"]
                for qa in paragraph["qas"]:
                    question_text = qa["question"]
                    for answer in qa["answers"]:
                        answer_text = answer["text"]
                        start_position_character = answer["answer_start"]
                        if question_text and answer_text and context_text and start_position_character:
                            example = QAExample(
                                question_text=question_text,
                                context_text=context_text,
                                answer_text=answer_text,
                                start_position_character=start_position_character,
                            )
                            examples.append(example)
        return examples
```

코드3의 `QADataset`은 파이토치의 데이터셋(`Dataset`) 클래스 역할을 하는 클래스입니다. 모델이 학습할 데이터를 품고 있는 일종의 자료 창고라고 이해하면 좋을 것 같습니다. 만약에 이번 학습에 $i$번째 문서-레이블이 필요하다고 하면 자료 창고에서 $i$번째 데이터를 꺼내 주는 기능이 핵심 역할입니다. 

학습을 본격적으로 시작하기 전 전처리 과정은 이렇습니다. `QADataset` 클래스를 선언할 때 코드1에서처럼 `corpus` 인자에 `QACorpus`를 넣었다면 `QADataset` 클래스는 코드2 `QACorpus`의 `get_examples` 메소드를 호출해 원본 데이터를 `QAExample` 형태로 읽어들입니다.


## **코드3** QADataset
{: .no_toc .text-delta }

```python
class QADataset(Dataset):

    def __init__(
            self,
            args: QATrainArguments,
            tokenizer: PreTrainedTokenizer,
            corpus: QACorpus,
            mode: Optional[str] = "train",
            convert_examples_to_features_fn=_squad_convert_examples_to_features,
    ):
        ...
            self.corpus = corpus
        ...
                examples = self.corpus.get_examples(corpus_fpath, mode)
                self.features = convert_examples_to_features_fn(examples, tokenizer, args)
        ...

    def __len__(self):
        return len(self.features)

    def __getitem__(self, i):
        return self.features[i]
```

`QADataset` 클래스는 이후 `convert_examples_to_features_fn` 함수를 호출해 앞서 읽어들인 `example`을 `feature`로 변환합니다. `convert_examples_to_features_fn`가 하는 역할은 `QAExample`를 모델이 학습할 수 있는 형태로 가공하는 것입니다. 다시 말해 문장을 토큰화하고 이를 인덱스로 변환하는 한편, 레이블 역시 정수(integer)로 바꿔주는 기능을 합니다.
이와 관련해 자세한 내용은 [7-2장 Training](https://ratsgo.github.io/nlpbook/docs/qa/train/)을 참고하면 좋을 것 같습니다.

한편 `QADataset` 클래스의 `convert_examples_to_features_fn` 인자로 기본값인 `_squad_convert_examples_to_features` 말고 다른 함수를 넣어줄 수도 있습니다.
이 경우 피처 구축은 해당 함수로 진행하게 됩니다. 단, 해당 함수의 결과물은 `List[QAFeatures]` 형태여야 합니다. 

`QAFeatures`의 구성 요소는 다음과 같습니다. `start_positions`는 정답의 시작 토큰 위치가 `input_ids` 시퀀스 가운데 몇 번째인지를 나타내는 자료입니다. `start_positions`는 정답의 마지막 토큰 위치를 나타냅니다.

- input_ids: `List[int]`
- attention_mask: `List[int]`
- token_type_ids: `List[int]`
- start_positions: `int`
- end_positions: `int`


---

## 다른 모델 사용하기

우리 책 질의 응답 튜토리얼에서는 이준범 님이 공개한 `kcbert`를 사용했습니다.
허깅페이스 라이브러리에 등록된 모델이라면 별다른 코드 수정 없이 다른 모델을 사용할 수 있습니다.
예컨대 `bert-base-uncased` 모델은 구글이 공개한 다국어 BERT 모델인데요.
`pretrained_model_name`에 해당 모델명을 입력하면 이 모델을 즉시 사용 가능합니다. 코드4와 같습니다.

## **코드4** 다른 모델 사용하기
{: .no_toc .text-delta }
```python
from ratsnlp.nlpbook.ner import QATrainArguments
from transformers import BertConfig, BertTokenizer, BertForQuestionAnswering
args = QATrainArguments(
    pretrained_model_name="bert-base-uncased",
    ...
)
tokenizer = BertTokenizer.from_pretrained(
    args.pretrained_model_name,
    do_lower_case=False,
)
pretrained_model_config = BertConfig.from_pretrained(
    args.pretrained_model_name,
)
model = BertForQuestionAnswering.from_pretrained(
    args.pretrained_model_name,
    config=pretrained_model_config,
)
```

허깅페이스에서 사용 가능한 모델 목록은 다음 링크를 참고하시면 됩니다.

- [https://huggingface.co/models](https://huggingface.co/models)

---

## 태스크 이해하기

우리 책 튜토리얼에서는 [파이토치 라이트닝(pytorch lightning)](https://github.com/PyTorchLightning/pytorch-lightning) 모듈을 상속 받아 태스크(task)를 정의합니다.
이 태스크에는 모델과 옵티마이저(optimizer), 학습 과정 등이 정의돼 있습니다. 코드5와 같습니다.

## **코드5** 질의 응답 태스크 정의
{: .no_toc .text-delta }

```python
from ratsnlp.nlpbook.ner import QATask
task = QATask(model, args)
```

`QATask`는 대부분의 질의 응답 태스크를 수행할 수 있도록 일반화되어 있어 말뭉치 등이 바뀌더라도 커스터마이즈를 별도로 할 필요가 없습니다. 
다만 해당 클래스가 어떤 역할을 하고 있는지 추가 설명이 필요할 것 같습니다. 
코드6은 코드5가 사용하는 `QATask` 클래스를 자세하게 나타낸 것입니다. 

코드6 태스크 클래스의 주요 메소드에 관한 설명은 다음과 같습니다.

- **configure_optimizers** : 모델 학습에 필요한 옵티마이저(optimizer)와 학습률(learning rate) 스케줄러(scheduler)를 정의합니다. 다른 옵티마이저와 스케줄러를 사용하려면 이 메소드의 내용을 고치면 됩니다.
- **training_step** : 학습(train) 과정에서 한 개의 미니배치(inputs)가 입력됐을 때 손실(loss)을 계산하는 과정을 정의합니다.
- **validation_step** : 평가(validation) 과정에서 한 개의 미니배치(inputs)가 입력됐을 때 손실(loss)을 계산하는 과정을 정의합니다.


## **코드6** 질의 응답 태스크 클래스
{: .no_toc .text-delta }

```python
from transformers import PreTrainedModel
from transformers.optimization import AdamW
from ratsnlp.nlpbook.metrics import accuracy
from pytorch_lightning import LightningModule
from ratsnlp.nlpbook.qa import QATrainArguments
from torch.optim.lr_scheduler import ExponentialLR


class QATask(LightningModule):

    def __init__(self,
                 model: PreTrainedModel,
                 args: QATrainArguments,
    ):
        super().__init__()
        self.model = model
        self.args = args

    def configure_optimizers(self):
        optimizer = AdamW(self.parameters(), lr=self.args.learning_rate)
        scheduler = ExponentialLR(optimizer, gamma=0.9)
        return {
            'optimizer': optimizer,
            'scheduler': scheduler,
        }

    def training_step(self, inputs, batch_idx):
        # outputs: QuestionAnsweringModelOutput
        outputs = self.model(**inputs)
        start_preds = outputs.start_logits.argmax(dim=-1)
        start_positions = inputs["start_positions"]
        end_preds = outputs.end_logits.argmax(dim=-1)
        end_positions = inputs["end_positions"]
        acc = (accuracy(start_preds, start_positions) + accuracy(end_preds, end_positions)) / 2
        self.log("loss", outputs.loss, prog_bar=False, logger=True, on_step=True, on_epoch=False)
        self.log("acc", acc, prog_bar=True, logger=True, on_step=True, on_epoch=False)
        return outputs.loss

    def validation_step(self, inputs, batch_idx):
        # outputs: QuestionAnsweringModelOutput
        outputs = self.model(**inputs)
        start_preds = outputs.start_logits.argmax(dim=-1)
        start_positions = inputs["start_positions"]
        end_preds = outputs.end_logits.argmax(dim=-1)
        end_positions = inputs["end_positions"]
        acc = (accuracy(start_preds, start_positions) + accuracy(end_preds, end_positions)) / 2
        self.log("val_loss", outputs.loss, prog_bar=True, logger=True, on_step=False, on_epoch=True)
        self.log("val_acc", acc, prog_bar=True, logger=True, on_step=False, on_epoch=True)
        return outputs.loss
```

코드6의 `training_step`, `validation_step` 메소드에선 미니 배치(input)를 모델에 태운 뒤 손실(loss)과 로짓(logit) 등을 계산합니다. 모델의 최종 출력은 '각 토큰이 정답의 시작/끝일 확률'인데요. 로짓은 소프트맥스를 취하기 직전의 벡터입니다. 

로짓(`outputs.logits`)에 argmax를 취해 모델이 예측한 시작/끝 토큰을 가려내고 이로부터 정확도(accuracy)를 계산합니다. 로짓으로 예측 범주(`preds`)를 만드는 이유는 소프트맥스를 취한다고 대소 관계가 바뀌는 것은 아니니, 로짓으로 argmax를 하더라도 예측 범주가 달라지진 않기 때문입니다. 이후 손실, 정확도 등의 정보를 로그에 남긴 뒤 메소드를 종료합니다.

코드6의 `training_step`, `validation_step` 메소드는 `self.model`을 호출(call)해 손실과 로짓을 계산하는데요. `self.model`은 코드7의 `BertForTokenClassification` 클래스를 가리킵니다. 본서에서는 허깅페이스의 [트랜스포머(transformers) 라이브러리](https://github.com/huggingface/transformers)에서 제공하는 클래스를 사용합니다. 그 핵심만 발췌한 코드는 코드7과 같습니다.

## **코드7** BertForQuestionAnswering
{: .no_toc .text-delta }

```python
class BertForQuestionAnswering(BertPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels

        self.bert = BertModel(config, add_pooling_layer=False)
        self.qa_outputs = nn.Linear(config.hidden_size, config.num_labels)

        self.init_weights()

    def forward(
        self,
        input_ids=None,
        attention_mask=None,
        token_type_ids=None,
        position_ids=None,
        head_mask=None,
        inputs_embeds=None,
        start_positions=None,
        end_positions=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
    ):
        ...

        outputs = self.bert(
            input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        sequence_output = outputs[0]

        logits = self.qa_outputs(sequence_output)
        start_logits, end_logits = logits.split(1, dim=-1)
        start_logits = start_logits.squeeze(-1)
        end_logits = end_logits.squeeze(-1)

        total_loss = None
        if start_positions is not None and end_positions is not None:
            # If we are on multi-GPU, split add a dimension
            if len(start_positions.size()) > 1:
                start_positions = start_positions.squeeze(-1)
            if len(end_positions.size()) > 1:
                end_positions = end_positions.squeeze(-1)
            # sometimes the start/end positions are outside our model inputs, we ignore these terms
            ignored_index = start_logits.size(1)
            start_positions.clamp_(0, ignored_index)
            end_positions.clamp_(0, ignored_index)

            loss_fct = CrossEntropyLoss(ignore_index=ignored_index)
            start_loss = loss_fct(start_logits, start_positions)
            end_loss = loss_fct(end_logits, end_positions)
            total_loss = (start_loss + end_loss) / 2

        ...

        return QuestionAnsweringModelOutput(
            loss=total_loss,
            start_logits=start_logits,
            end_logits=end_logits,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )
```

코드7의 `self.bert`는 [4-1장](https://ratsgo.github.io/nlpbook/docs/classification/overview)의 BERT 모델을 가리킵니다. 빈칸 맞추기, 즉 마스크 언어모델(Masked Language Model)로 프리트레인을 이미 완료한 모델입니다. `self.dropout`와 `self.classifier`는 7-1장에서 소개한 [질의 응답 태스크 모듈](http://localhost:4000/nlpbook/docs/qa/overview/)이 되겠습니다. KorQuAD 1.0 데이터에 대해 정답의 시작/끝 토큰 위치를 최대한 잘 맞추는 방향으로 `self.bert`, `self.classifier`가 학습됩니다.

한편 코드6의 `training_step`, `validation_step` 메소드에서 `self.model`을 호출하면 코드7 `BertForQuestionAnswering`의 `forward` 메소드가 실행됩니다. 다시 말해 코드6의 `training_step`, `validation_step` 메소드는 `self.model` 메소드와 짝을 지어 구현해야 한다는 이야기입니다. 


---
