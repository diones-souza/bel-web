# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 15:13:40 2018

@author: John
"""

import nltk
import random
import website.static.treatment  as treatment
import website.static.voice as voice
import website.models as models
from datetime import  timedelta
from sys import stdout
import time

'''
Previous essa função ser para retornarmos uma
possivel pre resposta para o usuario dependendo da
classificação feita pela analize
'''

def Previous(class_name):
    previous= []
    for data in base_previous:
        phrase = data.phrase
        if data.classification==class_name:
            previous.append(phrase)
    if class_name=='default':
        previous.append('')
    return previous

'''
Response essa função ser para retornarmos uma
resposta para o usuario
dentro da classificação feita pela analize
'''

def Response(class_name):
    response= []
    treatment.Treatment.ClassifyTreatment(class_name,response)
    for data in base_response:
        phrase = data.phrase
        if data.classification==class_name:
            response.append(phrase)
    if class_name=='default':
        response.append('Não entendi sua pergunta, poderia elaborar melhor?')
    return response

'''
Next essa função ser para retornarmos uma
possivel pos resposta para o usuario dependendo da
classificação feita pela analize
'''

def Next(class_name):
    nexts= []
    for data in base_next:
        phrase = data.phrase
        if data.classification==class_name:
            nexts.append(phrase)
    if class_name=='default':
        nexts.append('')
    return nexts

'''
GetUser retuna as informações do usuario exemplo: nome
'''

def GetUser(user,class_name):
    person = ''
    for data in user:
        phrase = data['frase']
        if data['classe']==class_name:
            person = phrase
    return person

'''
Tokenize essa função serve para quebrarmos
nosso texto por palavras, criando desse modo
um array com todas as palavras contidas dentro do texto.
Por exemplo, "Eu gosto de Correr" → ["eu","gosto","de","correr"]
'''

def Tokenize(sentence):
    #sentence = sentence.lower() #tranforma frase em minusculo
    sentence = nltk.word_tokenize(sentence)
    return sentence

'''
Tag utilizada para fazer a classificação adicional na frase essa função
verifica mais possibilidade de classe para a analise
a variavel user server para registrar entidades ou informaçoes que o usuario
passa
'''

def Tag(sentence,user):
    sentence = Tokenize(sentence)
    sentence = RemoveStopWords(sentence)
    tag = tagger.tag(sentence)
    print(tag)
    for phrase in tag:
        if phrase[1]=='NPROP':
            if phrase[0]!='Bel':
                user.append({"classe":"NPROP","frase":""+phrase[0]+""})


'''
Perceptron esse função serve para classificar
as palvras nas sua respectivas analise
ou seja faz a verificação se a palavra é um verbo, um Substantivo, Nome próprio etc.
'''

def Perceptron(base):
    tagger = nltk.tag.PerceptronTagger(False)
    tagger.train(base)
    return tagger

'''
Stemming: essa funçao serve para diminuirmos a palavra
ate a sua raiz/base, pois assim,
conseguimos tratar as palavras originais e
suas respectivas derivaçoes de uma mesma maneira.
Exemplo: As palavras Correr e Corrida
quando submetidas a nossa funçao de Stemming,
ambas as palavras serao diminuídas ate a base Corr.
'''

def Stemming(sentence):
    stemmer = nltk.RSLPStemmer()
    phrase = []
    for word in sentence:
        phrase.append(stemmer.stem(word.lower()))
    return phrase

'''
RemoveStopWords: essa funçao serve para retiramos
dentro do nosso array algumas palavras que nao sao
interessantes para contabilizarmos uma pontuaçao na hora
de classificar o nosso texto,
então mantemos somente as palavras principais.
'''

def RemoveStopWords(sentence):
    stopwords = nltk.corpus.stopwords.words('portuguese')
    phrase = []
    for word in sentence:
        if word not in stopwords:
            phrase.append(word)
    return phrase


'''
Learning: essa funçao é responsavel pelo treinamento

O parâmetro base, é o array contendo a base de treinamento.
Inicializamos um dicionario denominado corpus_words,
ele sera responsavel por armazenar as classes,
suas respectivas palavras e o peso de cada uma.
Logo apos, utilizamos um laço for para percorrer todos os elementos
dentro do array base.
Guardamos dentro de uma variavel denominada frase,
o valor correspondente da chave frase do array base,
e logo apos aplicamos os tres metodos auxiliares previamente desenvolvidos.
Guardados dentro de uma variável denominada class_name,
o valor correspondente ao nome da classe,
e criamos uma chave dentro de corpus_words com o nome da classe
caso ela nao exista.
E por ultimo criarmos um outro for que percorre as palavras,
caso a palavra ainda nao seja conhecida em nosso algorítimo a
inicializamos com o valor 1, e caso ela já seja conhecida adicionamos +1.
'''

def Learning(base):
    corpus_words = {}
    for data in base:
        phrase = data.phrase
        phrase = Tokenize(phrase)
        phrase = Stemming(phrase)
        phrase = RemoveStopWords(phrase)
        class_name = data.classification
        if class_name not in list(corpus_words.keys()):
            corpus_words[class_name] = {}
        for word in phrase:
            if word not in list(corpus_words[class_name].keys()):
                corpus_words[class_name][word] = 1
            else:
                corpus_words[class_name][word] += 1
    return corpus_words

'''
calculate_class_score: é solicitado como parametros uma frase
e uma classe na qual a frase sera comparada.
Em seguida possuímos a funçoes ja conhecidas, Tokenize e Stemming.
Apos a frase ser submetida à essas duas funçoes,
possuimos um laço for que é responsavel percorrer todas as
palavras da nossa frase e procurar dentro da classe informada as
frases que correspondem, calculando assim a quantidade total de pontos.
'''

def CalculateClassScore(sentence,class_name):
    score = 0
    sentence = Tokenize(sentence)
    sentence = Stemming(sentence)
    for word in sentence:
        if word in dados[class_name]:
            score += dados[class_name][word]
    return score


'''
calculate_score: funciona da seguinte maneira,
seu único parâmetro é a frase que queremos analisar.
Primeiramente inicializamos duas variáveis,
a high_score e nome da classe,
pois assim teremos algo para comparar
com o resultado do nosso classificador.
Logo após abrimos um laço for ,
que irá percorrer todas as 'keys' do nosso dicionário,
que em outras palavras são os nomes das nossas classes,
ao entrar no laço, temos uma variavel que é inicializada com o valor 0,
essa variável sera responsavel por armazenar
a quantidade de pontos que aquela frase obteve em relaçao
aquela classe. E isso será repetido ate nosso laço for percorrer
todas as classes contidas dentro do nosso dicionario.
e no final ela retornara o nome da classe que obteve
a maior quantidade de pontos.
'''

def CalculateScore(sentence):
    high_score = 0
    class_name = 'default'
    for classe in dados.keys():
        pontos = 0
        pontos = CalculateClassScore(sentence,classe)
        if pontos > high_score:
            high_score = pontos
            class_name = classe
    return class_name,high_score

'''
MarkTime função para marcar tempo
'''

def MarkTime():
    return time.time()

'''
Time função que calcula o tempo gasto das atividades feitas
pega a marcação inicial e final e calcula o tempo
'''
def Time(start,end):
    second = end - start
    now = timedelta(seconds=int(second))
    stdout.write("\r%s"%now)
    stdout.flush()

start = MarkTime()
base_class = models.Base_Classification.objects.all()
corpus = models.Corpus.objects.all()
tag=[]
for b in corpus:
    temp = [(b.word,b.classification)]
    tag.append(temp)

#incluir corpus mac_morpho na base de dados
'''
corpus = nltk.corpus.mac_morpho.tagged_sents()
for i in range(len(corpus)):
    for j in range(len(corpus[i])):
        try:
            temp = models.Corpus(word=str(corpus[i][j][0]),classification=str(corpus[i][j][1]))
            temp.save()
        except Exception as e:
            print(e)
'''
base_previous = models.Base_Previous.objects.all()
base_response = models.Base_Response.objects.all()
base_next = models.Base_Next.objects.all()
tagger = Perceptron(tag)
dados = Learning(base_class)
end = MarkTime()
Time(start,end)
print(' para treinamento')

class Main:       
    def Talk(message):
        start = MarkTime()
        person = []
        class_response = CalculateScore(message)
        class_name = class_response[0]
        Tag(message,person)
        person = GetUser(person,'NPROP')
        if person:
            class_name = 'NPROP'
        output=''
        try:
            previous = random.choice(Previous(class_name))
            if previous:
                output = previous+' '
        except Exception as e:
            print('Exception: '+str(e))
        try:
            responses = random.choice(Response(class_name))
            output+=responses
        except Exception as e:
            print('Exception: '+str(e))
        try:
            nexts = random.choice(Next(class_name))
            if nexts:
                output+=', '+nexts
        except Exception as e:
            print('Exception: '+str(e))
        if person:
            output+= ', '+person
        print('chat diz:'+output)
        voice.Voice.SetVoice(output)
        end = MarkTime()
        Time(start,end)
        print(' para resposta')
        if person:
            try:
                user = models.User(name=person)
                user.save()
            except Exception as e:
                print('Exception: '+str(e))
        try:
            log = models.Log(classification=class_name,input=message,output=output)
            log.save()
        except Exception as e:
            print('Exception '+str(e))
        return output
