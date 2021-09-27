// src/index.js
const { ApolloServer } = require('apollo-server-express') 
const express = require('express')
const resolvers = require( './graphql/resolvers')
const typeDefs = require('./graphql/typeDefs')
const expressPlayground = require('graphql-playground-middleware-express').default
var app = express()

// ApolloServer는 스키마와 리졸버가 반드시 필요함
const server = new ApolloServer({
  typeDefs,
  resolvers
});





async function startApolloServer() {
  try {
    await server.start()

    server.applyMiddleware({ app })
    app.get('/', (req, res)=>res.end('yaho'))
    app.get('/playground', expressPlayground({endpoint:'/graphql'}))
    app.listen({port:4000}, ()=>{console.log('run')})
  } catch(error){
  
    console.log('apollo error ' , error)
  }
  

}

startApolloServer()


