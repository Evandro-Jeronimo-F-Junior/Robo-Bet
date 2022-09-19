from datetime import datetime
import requests
from bs4 import BeautifulSoup
token = 'Adicionar seu token'
serie_a = {#adicionar aqui o site para a raspagem}
#abaixo eu tratei alguns dados
data_toda = str(datetime.now()).split()[0].split('-')[1:]
data_mes = int(data_toda[0])
data_dia = int(data_toda[1])
grupos = ['Adicionar o id de seus grupos do telegram']
headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
melhores_def_a = {}
melhores_def_b = {}
mensagem = {}
cont2 = 1

def Futebol(token, serie_a, grupos, cont2):
    for time, url in serie_a.items():  # for na s urls
        site = requests.get(url, headers=headers)  # pega a resposta
        soup = BeautifulSoup(site.content, 'html.parser')  # remove alguns inpecilios
        conteudo = soup.select('.homeTeamInfo .fs09e , #matchHistoryList .black')  # faz a seleçao do que eu quero
        jogos = dict()  # para adicionar os resultados das partidas anteriores
        contf = vitorias_f_casa = gols2 = cont = gols = gols_sofridos = total_gols_sofridos = total_gols_marcados = 0
        for indice, valor in enumerate(conteudo):  # pega as partidas
            if '-' in valor.text:
                jogos[conteudo[indice - 1].text + str(indice)] = valor.text
                cont += 1
            if cont == 10:
                break
        cont = 0
        for key, valor in jogos.items():  # linka os jogos de casa
            if '-' in valor:
                if time in key:  # se o time em questao joga em casa
                    cont += 1
                    if int(valor.split('-')[0]) > 0:
                        gols += 1
                        total_gols_marcados += int(valor.split('-')[0])
                        if int(valor.split('-')[0]) > 1:
                            gols2 += 1
                    if int(valor.split('-')[1]) > 0:
                        gols_sofridos += 1
                        total_gols_sofridos += int(valor.split('-')[1])
                else:  # se joga fora de casa
                    if int(valor.split('-')[1]) > 0:
                        gols += 1
                        total_gols_marcados += int(valor.split('-')[1])
                        if int(valor.split('-')[1]) > 1:
                            gols2 += 1
                    if int(valor.split('-')[0]) > 0:
                        gols_sofridos += 1
                        if int(valor.split('-')[0]) > 3:
                            total_gols_sofridos += 3
                        else:
                            total_gols_sofridos += int(valor.split('-')[0])
                    cont += 1
            if cont == 7:
                break
        for nome, placar in jogos.items():  # linka os jogos de casa
            if time in nome:  # se o time em questao joga em casa
                pass
            else:  # se joga fora de casa
                if int(placar.split('-')[1]) > int(placar.split('-')[0]):
                    vitorias_f_casa += 1
                contf += 1
            if contf == 4:
                break
        vitorias_f_casa = '{:.2f}'.format(vitorias_f_casa / contf * 100).replace('.', '\.')
        gols2 = '{:.2f}'.format(gols2 / cont * 100).replace('.', '\.')
        gols = '{:.2f}'.format(gols / cont * 100).replace('.', '\.')
        gols_sofridos = '{:.2f}'.format(gols_sofridos / cont * 100).replace('.', '\.')
        total_gols_marcados = '{:.2f}'.format(total_gols_marcados / cont).replace('.', '\.')
        total_gols_sofridos = '{:.2f}'.format(total_gols_sofridos / cont).replace('.', '\.')
        msg = f'O *__\({time}\)__* fazer: 1 gol *{gols}%* 2 gols *{gols2}%*, tomar 1 gol *{gols_sofridos}%* \nFaz em média *{total_gols_marcados}* e toma *{total_gols_sofridos}* \(Ganhar fora de casa *{vitorias_f_casa}%\)*\. '
        mensagem[time] = msg
        if cont2 <= 20:
            melhores_def_a[total_gols_sofridos + time] = time
        else:
            melhores_def_b[total_gols_sofridos + time] = time
        cont2 += 1
        print('feito')
    msg2 = ''
    msg3 = ''
    for defesa, time1 in sorted(melhores_def_a.items()):
        msg2 += f'*__{time1:<18}__* Nota: *{defesa[:5]}*\n'
    for defesa1, time2 in sorted(melhores_def_b.items()):
        msg3 += f'*__{time2:<18}__* Nota: *{defesa1[:5]}*\n'
    for b in range(7):
        requests.get(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={grupos[b]}&parse_mode=markdownv2&text=*Melhores defesas do campeonato serie a:\(Quanto menor a nota melhor\)*\n{msg2}')
        requests.get(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={grupos[b]}&parse_mode=markdownv2&text=*Melhores defesas do campeonato serie b:\(Quanto menor a nota melhor\)*\n{msg3}')

#o mes e os dias da rodada como abiaxo
rodada = {9: {19: ['Atlético GO', 'Internacional'],
          20: ['Grêmio', 'Sport Recife', 'Guarani', 'Novorizontino'],
          21: ['Cruzeiro', 'Vasco da Gama'],
          22: ['Vila Nova', 'CRB'],
          23: ['Náutico', 'Sampaio Corrêa', 'Londrina', 'Ponte Preta'],
          24: ['Ituano', 'Brusque', 'Bahia', 'Operário PR'],
          25: ['Criciúma', 'Chapecoense', 'São Paulo', 'Avaí']}}


def Dias(rodada, token):
    global data_dia, data_mes, data_toda
    Futebol(token, serie_a, grupos, cont2)
    for dias, chat_id in enumerate(grupos):
        if data_mes == 1 or data_mes == 3 or data_mes == 5 or data_mes == 7 or data_mes == 8 or data_mes == 10 or data_mes == 12:
            for times in rodada[data_mes][data_dia]:
                if times is None:
                    break
                requests.get(
                    f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=markdownv2&text={mensagem[times]}')
            if data_dia == 31:
                data_dia = 0
                data_mes += 1
            data_dia += 1
        elif data_mes == 4 or data_mes == 6 or data_mes == 9 or data_mes == 11:
            for times in rodada[data_mes][data_dia]:
                if times is None:
                    break
                requests.get(
                    f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=markdownv2&text={mensagem[times]}')
            if data_dia == 30:
                data_dia = 0
                data_mes += 1
            data_dia += 1
        elif data_mes == 2:
            if data_dia == 28:
                data_dia = 0
                data_mes += 1
                for times in rodada[data_mes][data_dia]:
                    if times is None:
                        break
                    requests.get(
                        f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=markdownv2&text={mensagem[times]}')
            data_dia += 1


Dias(rodada, token)
