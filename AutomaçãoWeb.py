#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
table = pd.read_excel(r'C:\Users\Mateus\Desktop\Cursos\Lira\Aula4\Produtos.xlsx')


driver.get('https://www.google.com.br/')

#pesquisar no google cotação dolar,euro e ouro

#dolar
driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('Cotação Dolar')
driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
dolar = driver.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')
#euro
driver.find_element_by_xpath('//*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input').send_keys(Keys.CONTROL+'A')
driver.find_element_by_xpath('//*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input').send_keys('Cotação Euro')
driver.find_element_by_xpath('//*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input').send_keys(Keys.ENTER)
euro = driver.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')
#ouro
driver.get('https://www.melhorcambio.com/ouro-hoje')
ouro = driver.find_element_by_xpath('//*[@id="comercial"]').get_attribute('value')
ouro = ouro.replace(',','.')

#passo 1: atualizar as cotações
table.loc[table['Moeda']=='Dólar','Cotação'] = float(dolar)
table.loc[table['Moeda']=='Euro','Cotação'] = float(euro)
table.loc[table['Moeda']=='Ouro','Cotação'] = float(ouro)

#passo 2: atualizar o preço base reais > cotação * preço base original
table['Preço Base Reais'] = table['Cotação']*table['Preço Base Original']

#passo 3: atualizar o preço final -> preço base reais * ajuste 
table['Preço Final'] = table['Preço Base Reais']*table['Ajuste']
table['Preço Final'] = table['Preço Final'].map('{:.2f}'.format)

table.to_excel(r'C:\Users\Mateus\Desktop\Cursos\Lira\Aula4\Produtos_Atualizados.xlsx', index=False)
driver.quit()

