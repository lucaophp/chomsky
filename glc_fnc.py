#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import string
import copy
import sys
'''
	ESTE SOFTWARE RODA TANTO NO PYTHON 2.x QUANTO NO 3.x
	EXEMPLO DE EXECUÇÃO EM BASH
		> python glc_fnc.py [caminho do arquivo de entrada] [caminho do arquivo de saida]
	SOFTWARE TOTALMENTE DESENVOLVIDO PELO GRUPO PARA A DISCIPLINA DE TEORIA DA COMPUTAÇÃO
		> Lucas Batista Fialho - 2712
		> Wisney Bernardes - 1285
		> Marciley Oliveira - 2768
'''
'''
	Classe Responsavel pela representação da Gramatica
	G=(V,T,P,S)
	V=variaveis
	T=terminais
	P=regraProducao(variavel,alpha)
	S= inicial
'''
class Gramatica:
	def __init__(self,variaveis,terminais,inicial):
		self.variaveis=list(variaveis)
		self.terminais=list(terminais)
		self.inicial=str(inicial)
		self.p={}
	def regraProducao(self,variavel,alpha):
		if variavel in self.p:
			prod=self.p[variavel]
			prod.append(alpha)
		else:
			self.p[variavel]=[alpha]
'''
	Classe Responsavel por fazer as operações necessarias para normalização de Chomsky da GLC passada por meio de arquivo.
	Passo 1:
		Variavel->apenas variaveis
		Variavel->apenas terminais
	Passo 2:
		Variavel->apenas duas ou uma variavel
		Variavel->apenas terminais

'''
class Chomsky:
	def __init__(self,gramatica):
		self.g=gramatica
	def converte(self):
		nGramatica=copy.copy(self.g)
		'''
			---------------------------------------------------------------
			Passo 1
			---------------------------------------------------------------
		'''
		for v in self.g.variaveis:
			if v not in self.g.p:
				continue
			for p in self.g.p[v]:
				contaVar=[]
				contaTer=[]
				for i,s in enumerate(p):
					if s in self.g.variaveis:
						contaVar.append([i,s])
					elif s in self.g.terminais:
						contaTer.append([i,s])
				
				if len(contaTer)!=0 and len(contaVar)!=0:
								
					for terPivo in contaTer:
							
								
						while True:
							newVar=random.choice(string.ascii_uppercase)
							if newVar not in self.g.variaveis:
								self.g.variaveis.append(newVar)
								break
							
						if terPivo[0]==len(p):
							string_nova=(p[0:terPivo[0]])+str(newVar)
							
						else:
							string_nova=(p[0:terPivo[0]])+str(newVar)+p[terPivo[0]+1:]
						
						
						self.g.regraProducao(newVar,terPivo[1])
						if p in self.g.p[v]:
							self.g.p[v][self.g.p[v].index(p)]=string_nova
							
						p=string_nova
		'''
			--------------------------------------------------------
			Passo 2
			--------------------------------------------------------
		'''
		#pega todas as produções com tres variaveis e reduz para duas.
		for v in self.g.variaveis:
			if v not in self.g.p:
				continue
			for i,p in enumerate(self.g.p[v]):
				while (len(p)>2):
					
					while True:
						newVar=random.choice(string.ascii_uppercase)
						if newVar not in self.g.variaveis:
							self.g.variaveis.append(newVar)
							break
					self.g.regraProducao(newVar,p[1:])
					self.g.p[v][i]=p[0]+newVar
					p=self.g.p[newVar][0]
				
		return self.g
class INOUT:
	def __init__(self,fileIN,fileOUT):
		self.fileInputName=fileIN
		self.fileOutputName=fileOUT
		self.readFile()

	def readFile(self):
		self.fileIN=open(self.fileInputName,'r')
		gramatica=Gramatica([],[],'')
		while True:
			linha=self.fileIN.readline()
			if (linha.split('#')[0].strip())=='GLC':
				status=True
				break
			elif (linha.split('#')[0].strip()) not in [' ','',None]:
				status=False
				break
		if status==False:
			return	
		#VERIFICO QUANTAS VARIAVEIS TEREMOS.
		while True:
			linha=self.fileIN.readline()
			if (linha.split('#')[0].strip()) not in [' ','',None,'0']:
				variaveis=range(0,int(linha.split('#')[0].strip()))
				break
		#leio as variaveis do arquivo.
		for v in variaveis:
			while True:
				linha=self.fileIN.readline()
				if (linha.split('#')[0].strip()) not in [' ','',None,'0']:
					gramatica.variaveis.append(str(linha.split('#')[0].strip()))
					break
		#leio quantos terminais teremos.
		while True:
			linha=self.fileIN.readline()
			if (linha.split('#')[0].strip()) not in [' ','',None,'0']:
				terminais=range(0,int(linha.split('#')[0].strip()))
				break
		#preencho a lista de terminais.
		for t in terminais:
			while True:
				linha=self.fileIN.readline()
				if (linha.split('#')[0].strip()) not in [' ','',None]:
					gramatica.terminais.append(str(linha.split('#')[0].strip()))
					break
		#percorro o arquivo ate terminar pegando as produções
		while True:
			try:
				#primeiro pegamos uma variavel.
				while True:
					linha=self.fileIN.readline()
					if not linha: break
					if (linha.split('#')[0].strip()) not in [' ','',None]:
						variavel=(str(linha.split('#')[0].strip()))
						break
				
				#pegamos o lado direito da produção.
				while True:
					linha=self.fileIN.readline()
					if not linha: break
					if (linha.split('#')[0].strip()) not in [' ','',None]:
						alpha=(str(linha.split('#')[0].strip()))
						break
				if not linha: break
				#monto uma produção.
				gramatica.regraProducao(variavel,alpha)
			except EOFError, e:
				break
		self.fileIN.close()
		#self.fileOUT.close()
		gramatica.inicial=gramatica.variaveis[0]
		return gramatica
	def save(self,gramatica):
		self.fileOUT=open(self.fileOutputName,'w')
		self.fileOUT.write("GLC\t# identifica o tipo de formalismo\n")
		self.fileOUT.write(str(len(gramatica.variaveis))+"\t# quantidade de variaveis\n")
		for v in gramatica.variaveis:
			self.fileOUT.write(str(v)+'\n')
		self.fileOUT.write(str(len(gramatica.terminais))+"\t# quantidade de símbolos terminais\n")
		for t in gramatica.terminais:
			self.fileOUT.write(str(t)+'\n')
		self.fileOUT.write('# Listagem de Regras de Produção\n')
		for lado_esquerdo in gramatica.p:
			for i,lado_direito in enumerate(lado_esquerdo):
				
				self.fileOUT.write(str(lado_esquerdo)+'\n')
				self.fileOUT.write(str(gramatica.p[lado_esquerdo][i])+'\t #'+str(lado_esquerdo)+'->'+str(gramatica.p[lado_esquerdo][i])+'\n')


		

		self.fileOUT.close()
if len(sys.argv)<2:
	print('Entradas apenas por terminal!!!')
i=INOUT(sys.argv[1],sys.argv[2])
g=i.readFile()										
c=Chomsky(g)
print('Gramatica não normalizada \n %s\n'%g.p)
g=c.converte()
i.save(g)
print('Gramatica normalizada por Chomsky: \n %s\n'%g.p)
