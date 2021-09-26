import keep_alive
import time
from datetime import datetime
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import geckodriver_autoinstaller
import sys
import sqlite3
import emoji
from pytz import timezone
import threading 
from cryptography.fernet import Fernet
import os


global chat_ids

my_secret = os.environ['senha']
my_secret_chave_bot = os.environ['chave_bot']
my_secret_id_canal = os.environ['id_canal']
my_secret_id_meu_telegram = os.environ['id_meu_telegram']
my_secret_id_telegram_neis = os.environ['id_telegram_neis']

geckodriver_autoinstaller.install()

bot = telepot.Bot(my_secret_chave_bot)

channel_id = my_secret_id_canal
chat_ids = [
  my_secret_id_meu_telegram, my_secret_id_telegram_neis
]


def enviar():
	driver = webdriver.Firefox()
	driver.get("http://www.python.org")
	bot.sendMessage(chat_id, 'Foi', parse_mode='Markdown')


def Deletar(id):
  conn = sqlite3.connect('python.db')
  c = conn.cursor()
  #c.execute('DROP TABLE Agenda')
  print(id)
  c.execute('DELETE FROM Agenda WHERE ID='+ id )
  c.close
  conn.commit()
  conn.close
  bot.sendMessage(chat_id, "Você apagou o lembrete: "+ id ,parse_mode="Markdown")


def CriarTabela():
	conn = sqlite3.connect('python.db')
	c = conn.cursor()
	c = c.execute('PRAGMA encoding="UTF-8";')
	c.execute(
	    'CREATE TABLE IF NOT EXISTS Agenda (id INTEGER PRIMARY KEY , lembrete VARCHAR(500))'
	)
	c.close
	conn.close

CriarTabela()

def Inserir(lembrar):
	conn = sqlite3.connect('python.db')
	c = conn.cursor()
	c = c.execute('PRAGMA encoding="UTF-8";')
	c.execute("INSERT INTO Agenda (lembrete) VALUES(?)", (lembrar, ))
	conn.commit()
	c.close
	conn.close


def Selecionar():
  conn = sqlite3.connect('python.db')
  c = conn.cursor()
  cur = conn.cursor()
  cur.execute("SELECT * FROM Agenda")
  rows = cur.fetchall()
  lembrete = ""
  for row in rows:
    print(row)
    lembrete = lembrete + str(row[0]) + " - " + str(row[1]) + "\n"

  if lembrete != '':
    bot.sendMessage(chat_id, str(lembrete), parse_mode="Markdown")
    
  cur.close
  c.close
  conn.close


def handle(msg):
  global chat_id
  content_type, chat_type, chat_id = telepot.glance(msg)
  content_type = telepot.glance(msg)
  global response
  response = bot.getUpdates()
  manutencao = False
  send1 = msg['text'][0:500]
  print(send1)
  if send1:
    text1 = send1
    if text1[0:6] == "/start":
      print("MensagemInicial")
      MensagemInicial()
    elif text1[1:7] == "Provas":
      VerificaProvas()
    elif text1[1:7] == "Agenda":
      Selecionar()
    elif text1[1:8] == "Deletar":
      ItensDeletar()
      #DeletarTab()
    elif text1[1:7] == "Ativos":
      Ativos()
    elif text1[1:4] == "Loop":
      Ativos()
    elif text1[0:6] == "Senha:":
      global senha
      senha = text1[6:500]
    elif text1[0:4] == 'Del:':
      Deletar(text1[4:7])
    elif text1[0:10] == 'Atividades':
      VerificaAtividades()
    else:
      Inserir(str(text1[0:500]))
      Selecionar()


global PrimeiroLogin
PrimeiroLogin = True

MessageLoop(bot, handle).run_as_thread()

from selenium.webdriver.firefox.options import Options



options = Options()
#options.headless = True
driver = webdriver.Firefox(options=options)

def ItensDeletar():
  conn = sqlite3.connect('python.db')
  c = conn.cursor()
  cur = conn.cursor()
  cur.execute("SELECT * FROM Agenda")

  rows = cur.fetchall()
  lembrete = ""
  for row in rows:
    lembrete = str(row[0]) + str(" - ") + row[1]
    bot.sendMessage(chat_id,'___________________________________________________',reply_markup = InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton(text=emoji.emojize("Del:"+str(lembrete)+" "),callback_data=str(lembrete[0:10])),
                                ]]
                            ))
    #print(row)

  cur.close
  c.close
  conn.close

def Ativos():
  Valores = ""
  bot.sendMessage(chat_id, "Verificando os valores dos seus ativos", parse_mode="Markdown")
  driver.get("https://dolarhoje.com/iota/")
  valor = driver.find_element_by_id("nacional").get_attribute('value')
  Valores = Valores + "Valor da IOTA :*R$" + str(valor) + "*\n"
  driver.get("https://dolarhoje.com/dogecoin-hoje/")
  valor = driver.find_element_by_id("nacional").get_attribute('value')
  Valores = Valores + "Valor do DODGE :*R$" + str(valor) + "*\n"
  bot.sendMessage(chat_id, Valores, parse_mode="Markdown")


def Looop():
  while loop == True:
    valor = 0
    driver.get("https://dolarhoje.com/iota/")
    valor = driver.find_element_by_id("nacional").get_attribute('value')
    if (float(valor.replace(',', '.')) >= 10.50):
      for chat_id in chat_ids:
        Valores = "*ATENÇÃO*\n\nValor da IOTA :*R$" + str(valor) + ", valor bom para a venda*\n"
        bot.sendMessage(chat_id, Valores, parse_mode="Markdown")

    driver.get("https://dolarhoje.com/dogecoin-hoje/")
    valor = driver.find_element_by_id("nacional").get_attribute('value')
    if (float(valor.replace(',', '.')) >= 1.95):
      for chat_id in chat_ids:
        Valores = "*ATENÇÃO*\n\nValor do DODGE :*R$" + str(valor) + ", valor bom para a venda*\n"
        bot.sendMessage(chat_id, Valores, parse_mode="Markdown")
    time.sleep(3600)


def VerificaAtividades():
  VerificaProvas()
  bot.sendMessage(chat_id, "Verificando suas atividades", parse_mode="Markdown")
  driver.get("https://ava.univesp.br/ultra/stream")
  time.sleep(2)
  cli = driver.find_element_by_id("agree_button").click()
  try:
    driver.find_element_by_class("button-1").click()
  except:
    pass
  time.sleep(2)
  cli = driver.find_element_by_id("sou-container").click()
  time.sleep(10)
  a = driver.find_elements_by_xpath("//ul[@class='activity-feed']//a")
  #for b in driver.find_elements_by_xpath("//a/following-sibling::b"):
  time.sleep(15)
  print("foi")
  a = driver.find_elements_by_xpath("//ul[@class='activity-feed']//a")
  texto =""
  for b in driver.find_elements_by_xpath("//ul[@class='activity-feed']//a"):
    texto = texto + b.text +"\n"
    print(b.text)
  bot.sendMessage(chat_id, texto, parse_mode="Markdown")

def VerificaProvas():
  if senha == "":
    bot.sendMessage(chat_id, "Envie a senha", parse_mode="Markdown")
    return
  global PrimeiroLogin
  bot.sendMessage(chat_id, "Verificando suas provas", parse_mode="Markdown")
  driver.get("https://apps.univesp.br/minhasprovas/")
  if PrimeiroLogin == True:
    print("Entrou")
    email = driver.find_element_by_name("username")
    # print("Element is visible? " + str(email.is_display()))
    driver.implicitly_wait(10)
    email.send_keys("1806217@aluno.univesp.br")
    email.send_keys(Keys.RETURN)
    senhas = driver.find_element_by_name("password")
    senhas.send_keys(senha)
    senhas.send_keys(Keys.RETURN)
    time.sleep(2)
  datas = driver.find_elements_by_css_selector(
      "#tabela div.linha div.dataDscpln span")
  dataHoje = datetime.today().strftime('%d/%m/%Y')
  print("data de hoje " + str(dataHoje))
  PrimeiroLogin = False

  temprova = False

  linha = 0
  dataHoje = datetime.strptime(dataHoje, '%d/%m/%Y')
  for data in datas:
    if (linha >= 1):
      print(str(linha))
      if data.text != "DATA" and data.text != "Data" and data.text != "data":
        data = str(data.text)
        data = datetime.strptime(data, '%d/%m/%Y')
        
        print("Data hoje "+ str(dataHoje))
        print("data "+str(data))
        if data == dataHoje:
          bot.sendMessage(chat_id,
                          "Hoje tem prova",
                          parse_mode='Markdown')
          temprova = True
        elif data > dataHoje:
          bot.sendMessage(chat_id,
                          "*ATENÇÃO*\n\nVocê tem prova dia " +
                          str(format(data, '%d/%m/%Y')),
                          parse_mode='Markdown')
          temprova = True
    linha = linha + 1
  if temprova == False:
    bot.sendMessage(chat_id,
                    "Nenhuma prova programada para UNIVESP",
                    parse_mode='Markdown')
    
def MensagemInicial():
  bot.sendMessage(
      chat_id,
      'Bem vindo(a) '+str(response[0][u'message'][u'from'].get(u'first_name'))+"\n\nPara registrar uma nova tarefa basta me enviar por escrito;\nUtilize os botões para:\n     Verificar sua agenda\n     Verificar suas provas\n     Verificar os valores dos seus ativos\n     Deletar tarefas da agenda",
      reply_markup=ReplyKeyboardMarkup(keyboard=[[
          KeyboardButton(text=emoji.emojize(":calendar:Agenda")),
          KeyboardButton(text=emoji.emojize(":open_book:Provas")),
          KeyboardButton(text=emoji.emojize(":money_bag:Ativos")),
          KeyboardButton(
              text=emoji.emojize(":counterclockwise_arrows_button:Deletar")),
          KeyboardButton(
              text=emoji.emojize(":counterclockwise_arrows_button:Loop")),
      ]]))

HoraLembrete = '17:47:00'
HoraLembrete = '17:47:02'

global loop
loop = True
t1 = threading.Thread (target = Looop) 
t1.start() 



senha = my_secret

while True:
  Agora = datetime.now(timezone('Brazil/East'))
  HoraAgora = Agora.strftime("%H:%M:%S")
  #print(HoraAgora)
  #print(HoraLembrete)
  if HoraAgora >= HoraLembrete and HoraAgora <= HoraLembrete:
    for chat_id in chat_ids:
      chat_id = chat_id
      VerificaProvas()
  time.sleep(1)
