#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

settings_json = json.dumps([
	{
	'type':'title',
	'title':'Configuração do Onnix Force'
	},
	{
	'type':'string',
	'title':'Usuário',
	'desc':'Idenfificação do Usuário para acessar o Onnix Force',
	'section':'onnixforce',
	'key':'username',
	},
	{
	'type':'string',
	'title':'Senha',
	'desc':'Senha para acessar o Onnix Force',
	'section':'onnixforce',
	'key':'password',
	},
	{
	'type':'string',
	'title':'Servidor',
	'desc':'Servidor de Integração do Onnix Force',
	'section':'onnixforce',
	'key':'api_hostname',
	},
	{
	'type':'string',
	'title':'Caminho da API',
	'desc':'Caminho da API de Integração do Onnix Force',
	'section':'onnixforce',
	'key':'api_endpoint',
	},
	{
	'type':'string',
	'title':'Região de Venda',
	'desc':'Estados onde o representante atua (separados por espaço)',
	'section':'onnixforce',
	'key':'states',
	},
	{
	'type':'string',
	'title':'Ultima atualização de clientes',
	'desc':'Ultima atualização de clientes obtida do servidor',
	'section':'onnixforce',
	'key':'customer_update_server',
	},
	{
	'type':'string',
	'title':'Ultima atualização de produtos',
	'desc':'Ultima atualização de produtos obtida do servidor',
	'section':'onnixforce',
	'key':'product_update_server',
	},
	])
