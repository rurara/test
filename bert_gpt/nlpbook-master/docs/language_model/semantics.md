---
layout: default
title: Pretrained LM
parent: Language Model
nav_order: 1
---

# 미리 학습된 언어 모델
{: .no_toc }

최근 BERT, GPT 같은 모델이 주목을 받게 된 이유는 성능 때문입니다. 이 모델들을 사용하면 문서 분류, 개체명 인식 등 어떤 태스크든지 점수가 이전 대비 큰 폭으로 오르기 때문인데요. BERT, GPT 따위의 부류는 **미리 학습된 언어 모델(pretrained language model)**이라는 공통점이 있습니다. 이 절에서는 언어 모델의 개념과 프리트레인의 종류, 프리트레인을 마친 언어모델이 성능이 좋은 이유 등을 살펴보고자 합니다.
{: .fs-4 .ls-1 .code-example }

## Table of contents
{: .no_toc .text-delta .mt-6}

1. TOC
{:toc}

---

## 언어 모델

**언어 모델(Language Model)**이란 <u>단어 시퀀스에 확률을 부여하는 모델</u>입니다. 다시 말해 단어 시퀀스를 입력받아 해당 시퀀스가 얼마나 그럴듯한지 확률을 출력으로 하는 모델입니다. 따라서 한국어 말뭉치로 학습한 언어 모델은 자연스러운 한국어 문장에 높은 확률값을 부여합니다. 어떤 문장이 한국어스러운지 해당 모델이 이해하고 있다는 것이죠.

문장에서 $i$번째로 등장하는 단어를 $w_i$로 표시한다면 $n$개 단어로 구성된 문장이 해당 언어에서 등장할 확률, 즉 언어 모델의 출력은 수식1과 같이 쓸 수 있습니다. 이 수식은 $n$개 단어가 동시에 나타날 **결합확률(joint probability)**을 의미합니다. 잘 학습된 한국어 언어모델이 있다면 $P(무모, 운전)$보다는 $P(난폭, 운전)$\*이 큰 확률값을 지닐 겁니다.

\* '난폭'이라는 단어와 '운전'이라는 단어가 동시에 나타날 결합 확률이라는 뜻입니다.
{: .fs-4 .ls-1 .code-example }

## **수식1** 언어 모델
{: .no_toc .text-delta }

$$
P(w_1, w_2, w_3, w_4, w_5, ... ,w_n)
$$

그렇다면 `난폭`이라는 단어가 나타난 다음에 `운전`이라는 단어가 나타날 확률은 어떻게 정의할까요? 이러한 확률을 **조건부 확률(conditional probability)**이라고 하는데요. 수식2와 같이 정의됩니다.

## **수식2** '난폭' 다음에 '운전'이 올 조건부 확률
{: .no_toc .text-delta }

$$
P(운전 | 난폭)=\frac { P(난폭, 운전) }{ P(난폭) } 
$$

조건부 확률(위 수식 좌변)을 표기할 때 결과가 되는 사건(`운전`)을 앞에, 조건이 되는 사건(`난폭`)은 뒤에 씁니다. 조건이 되는 사건이 우변 분자의 일부, 그리고 우변 분모를 구성하고 있음을 볼 수 있는데요. 이는 결과가 되는 사건(`운전`)은 조건이 되는 사건(`난폭`)의 영향을 받아 변한다는 개념을 내포하고 있습니다. 그도 그럴 것이 앞선 단어가 `난폭`이라면 다음 단어로 어떤 것이 자연스러울지 그 선택지가 확 줄어들겠죠.

결합확률과 조건부 확률 사이에는 밀접한 관련이 있습니다. 조건부 확률 정의에 따라 단어 3개가 동시에 등장할 결합확률을 수식으로 나타내면 다음과 같습니다.

## **수식3** 결합 확률과 조건부 확률 사이의 관계
{: .no_toc .text-delta }

$$
P(w_1,w_2,w_3)=P(w_1)\times P(w_2 | w_1)\times P(w_3 | w_1,w_2)
$$

수식2의 조건부 확률의 정의에 따라 수식3의 우변을 쭉 펼쳐 계산해보면 수식3 좌변과 같습니다. 이를 직관적으로 곱씹어보면, 단어 3개로 구성된 문장이 나타나려면(즉, 단어 3개가 동시에 등장하려면) 아래 3개 **사건(event)**이 동시에 일어나야 한다는 말이 됩니다.

- 첫번째 단어($w_1$)가 등장
- 첫번째 단어($w_1$)가 등장한 후 두번째 단어($w_2$)가 등장
- 첫번째 단어($w_1$)와 두번째 단어($w_2$)가 등장한 후 세번째 단어($w_3$)가 등장

이로부터 수식1의 언어모델을 조건부 확률 개념으로 다시 쓰면 다음 수식과 같습니다. 요약하면 **전체 단어 시퀀스가 나타날 확률**(다음 수식 좌변)은 **이전 단어들이 주어졌을 때 다음 단어가 등장할 확률의 연쇄**(다음 수식 우변)와 같다는 이야기입니다. 이 때문에 언어 모델을 <u>이전 단어들이 주어졌을 때 다음 단어가 나타날 확률을 부여하는 모델</u>이라고 정의하기도 합니다.


## **수식3** 조건부 확률로 다시 쓴 언어 모델
{: .no_toc .text-delta }

$$
P(w_1, w_2, w_3, w_4, ... w_n) = \prod_{i=1}^{n}P(w_{i} | w_{1}, ... , w_{i-1})
$$


### 순방향 언어 모델

우리는 임의의 단어 시퀀스가 해당 언어에서 얼마나 자연스러운지 이해하고 있는 언어 모델을 구축하려고 합니다. 그런데 조건부 확률의 정의에 따라 수식3의 좌변과 우변이 같다는 사실을 알고 있으므로 언어 모델의 계산 로직을 **이전 단어들(컨텍스트)가 주어졌을 때 다음 단어 맞추기**로 정해도 목표를 달성할 수 있습니다.

그림1은 학습 말뭉치가 `어제 카페 갔었어 거기 사람 많더라`라는 문장 하나일 때 언어 모델이 계산하는 대상을 나타낸 것입니다. 회색 단어는 컨텍스트, 붉은색 단어는 맞혀야할 다음 단어를 의미합니다. 이처럼 문장 앞부터 뒤로, 사람이 이해하는 순서대로 계산하는 모델을 **순방향(forward) 언어모델**이라고 합니다. GPT, ELMo 같은 모델이 이같은 방식으로 프리트레인을 수행합니다.

## **그림1** 순방향(left-to-right) 언어모델
{: .no_toc .text-delta }
<img src="https://i.imgur.com/4dv6TNZ.png" width="400px" title="source: imgur.com" />


### 역방향 언어 모델

그림2는 같은 데이터지만 문장 뒤부터 앞으로 계산하는 **역방향(backward) 언어 모델**을 나타내고 있습니다. 역방향 언어모델 역시 방향만 바뀌었을 뿐 다음 단어 맞추기 과정에서 전체 단어 시퀀스가 나타날 확률을 계산할 수 있습니다. [ELMo](https://allennlp.org/elmo)\* 같은 모델이 이같은 방식으로 프리트레인을 수행합니다

\* ELMo(Embeddings from Language Models)는 순방향과 역방향 언어 모델 모두 활용하는 기법입니다.
{: .fs-4 .ls-1 .code-example }

## **그림2** 역방향(right-to-left) 언어모델
{: .no_toc .text-delta }
<img src="https://i.imgur.com/VHB5dsR.png" width="400px" title="source: imgur.com" />

---

## 넓은 의미의 언어모델

전통적인 의미의 언어모델은 수식3처럼 정의했지만 최근에는 다음 수식처럼 정의하기도 합니다.

## **수식4** 넓은 의미의 언어 모델
{: .no_toc .text-delta }

$$
P(w | \text{context} )
$$

이는 컨텍스트(context; 주변 맥락 정보)가 전제된 상태에서 특정 단어($w$)가 나타날 조건부 확률을 나타냅니다. 이렇게 정의된 언어모델은 단어 혹은 단어 시퀀스로 구성된 컨텍스트를 입력 받아 특정 단어가 나타날 확률을 출력합니다. 이때 컨텍스트와 맞힐 단어를 어떻게 설정하느냐에 따라 다양하게 변형할 수 있습니다.


### 마스크 언어모델

**마스크 언어모델(Maksed Language Model)**은 학습 대상 문장에 빈칸을 만들어 놓고 해당 빈칸에 올 단어로 적절한 단어가 무엇일지 분류하는 과정으로 학습합니다. BERT가 마스크 언어모델로 프리트레인되는 대표적인 모델입니다. 그림3은 마스크 언어모델을 나타낸 것입니다.

## **그림3** 마스크 언어모델
{: .no_toc .text-delta }
<img src="https://i.imgur.com/YJjh69r.png" width="400px" title="source: imgur.com" />

그림3의 첫번째 줄에서 컨텍스트는 `[MASK] 카페 갔었어 거기 사람 많더라`이고 맞힐 대상이 되는 단어는 `어제`입니다. 마찬가지로 두번째 줄의 컨텍스트는 `어제 [MASK] 갔었어 거기 사람 많더라`이며 맞힐 단어는 `카페`입니다. 즉 회색 단어는 컨텍스트, 붉은색 단어는 맞혀야 할 타깃 단어를 가리킵니다. 

맞힐 단어 이전 단어들만 참고할 수 있는 순방향/역방향 언어모델과 달리 마스크 언어 모델은 맞힐 단어를 계산할 때 문장 전체의 맥락을 참고할 수 있다는 장점이 있습니다. 이 때문에 마스크 언어모델에 양방향(bidirectional) 성질이 있다고들 합니다. 다시 말해 맞힐 단어 앞뒤를 모두 본다는 뜻입니다.


### 스킵-그램 모델

스킵-그램 모델(Skip-Gram Model)은 어떤 단어 앞뒤에 특정 범위를 정해 두고 이 범위 내에 어떤 단어들이 올지 분류하는 과정에서 학습합니다. 다음 그림은 컨텍스트로 설정한 단어(파란색 네모칸) 앞뒤로 두 개씩 보는 상황을 나타낸 예시입니다. 

## **그림5** 스킵-그램 모델
{: .no_toc .text-delta }
<img src="https://i.imgur.com/tVEaCtD.png" width="400px" title="source: imgur.com" />

이때 스킵-그램 모델은 `갔었어` 주변에 `어제`, `카페`, `거기`, `사람`이 나타날 확률을 각각 높이는 방식으로 학습합니다. 그다음에 `거기` 주변에 `카페`, `갔었어`, `사람`, `많더라`가 나타날 확률을 각각 높입니다. 즉 스킵-그램 모델은 컨텍스트로 설정한 단어 주변에 어떤 단어들이 분포해 있는지를 학습한다는 이야기입니다. 2013년 구글에서 발표한 단어 수준 임베딩 기법인 [Word2Vec](https://github.com/tmikolov/word2vec)이 스킵-그램 모델 방식으로 학습합니다.

---

## 언어 모델의 유용성

잘 학습된 언어모델은 어떤 문장이 자연스러운지 가려낼 수 있어 그 자체로 값어치가 있습니다. 학습 대상 언어의 풍부한 맥락을 포함하고 있다는 점 역시 큰 장점입니다. 이 때문에 기계 번역, 문법 교정, 문장 생성 등 다양한 태스크를 수행할 수 있습니다.

- 기계 번역 : $P(\text{?}\|\text{죽음으로부터 자유로울 수 없다})$
- 문법 교정 : $P(\text{두시 삼십 이분})$ > $P(\text{이시 서른 두분})$
- 문장 생성 : $P(\text{?}\|\text{발 없는 말이})$

그림4는 이준범 님이 공개한 [kcbert-large 모델의 계산 결과](https://huggingface.co/beomi/kcbert-large)입니다. 이 모델은 12기가바이트(GB) 크기의 네이버 댓글 데이터로 학습한 BERT인데요. 마스크 언어모델 방식으로 프리트레인을 했습니다.

## **그림4** kcbert-large 모델의 계산 결과
{: .no_toc .text-delta }
<img src="https://i.imgur.com/ecigp05.png" width="400px" title="source: imgur.com" />

이 모델에 `어제 카페 갔었어 [MASK] 사람 많더라`를 입력하니 해당 마스크 위치에 `.`(확률값 0.131)이 오는 것이 가장 자연스럽다고 예측하고 있군요. `?`(0.119), `생각보다`(0.106), `~`(0.092), `어쩐지`(0.054) 등이 그 뒤를 잇고 있습니다. 모두 그럴듯한 한국어 문장임을 확인할 수 있습니다.

그림5는 OpenAI가 2020년 공개한 대규모 언어 모델인 GPT3의 단순 계산 능력을 평가한 그래프입니다. '다음 단어 맞히기'라는 단순 태스크로만 프리트레인을 했음에도 가장 큰 모델인 `175B`\*는 두 자릿수 덧셈/뺄셈에서 거의 100%에 가까운 정확도를 나타내고 있습니다. 해당 모델이 학습 말뭉치를 그대로 외운 것 같다는 인상을 주지만, 큰 언어모델에 학습 대상 언어의 풍부한 맥락이 내재화되어 있다는 점은 의심할 여지가 없습니다.

\* 모델의 파라미터(parameter) 수가 175Billion, 즉 1,750억 개라는 뜻입니다. 모델 파라미터는 행렬이나 벡터인데요. 파라미터 수는 행렬, 벡터 요소 수의 총합을 가리킵니다. 파라미터 수가 많을수록 큰 모델이라는 뜻입니다.
{: .fs-4 .ls-1 .code-example }

## **그림5** GPT3의 단순 계산 능력
{: .no_toc .text-delta }
<img src="https://i.imgur.com/FjrJwCS.png" width="400px" title="source: imgur.com" />

최근 들어 언어모델이 주목받고 있는 이유 가운데 하나는 데이터 제작 비용 때문입니다. '다음 단어 맞히기'나 '빈칸 맞히기' 등으로 학습 태스크를 구성하면 사람이 일일이 수작업해야 하는 레이블 없이도 많은 학습 데이터를 싼값에 만들어낼 수 있습니다. GPT3 같은 대규모 언어 모델이 탄생하게 된 배경이기도 하죠.

또다른 이유는 [트랜스퍼 러닝(Transfer Learning)](https://ratsgo.github.io/nlpbook/docs/introduction/transfer)을 꼽을 수 있습니다. 대량의 말뭉치로 프리트레인한 언어모델을 문서 분류, 개체명 인식 등 다운스트림 태스크에 적용하면 적은 양의 데이터로도 그 성능을 큰폭으로 올릴 수 있습니다. 

실제로 자연어 처리 분야에서 최근 제안되는 기법들은 프리트레인을 마친 딥러닝 계열 언어 모델을 바탕으로 할 때가 많습니다. 이 언어모델의 최종 혹은 중간 출력값을 가지고 다양한 태스크를 수행합니다. 이러한 출력값을 **임베딩(embedding)** 혹은 **리프레젠테이션(representation)**이라고 부릅니다. 


---