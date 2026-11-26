import os
import time
from datetime import datetime, timedelta

import pandas as pd
import pyautogui
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.options import Options

load_dotenv()

TEMPO_DE_ESPERA = 0.7

LOGIN = os.getenv("AGENDAMENTO_LOGIN", "")
SENHA = os.getenv("AGENDAMENTO_SENHA", "")
URL_SISTEMA = os.getenv("AGENDAMENTO_URL", "https://sistema-exemplo.invalid")
CNPJ_FIXO = os.getenv("AGENDAMENTO_CNPJ", "00000000000000")
NAVIO_FIXO = os.getenv("AGENDAMENTO_NAVIO", "NAVIO EXEMPLO")

ARQUIVO_EXCEL = "dados_agendamento_exemplo.xlsx"
NOME_PLANILHA = "AGENDAMENTOS"

if not LOGIN or not SENHA:
    raise RuntimeError(
        "Configure AGENDAMENTO_LOGIN e AGENDAMENTO_SENHA no arquivo .env local."
    )

chrome_options = Options()

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20)


def salvar_planilha(dataframe):
    """Salva a planilha de demonstração/execução."""
    dataframe.to_excel(
        ARQUIVO_EXCEL,
        sheet_name=NOME_PLANILHA,
        index=False,
    )


try:
    driver.get(URL_SISTEMA)
    time.sleep(2)

    driver.find_element(By.ID, "CNPJ").send_keys(LOGIN)
    driver.find_element(By.NAME, "Password").send_keys(SENHA)
    driver.find_element(By.NAME, "access").click()

    time.sleep(8)

    df = pd.read_excel(
        ARQUIVO_EXCEL,
        sheet_name=NOME_PLANILHA,
        dtype=str,
    )
    df.columns = df.columns.str.upper().str.strip()

    for index, linha in df.iterrows():
        status_atual = str(linha.get("STATUS", "")).strip().upper()

        print(f"Lendo linha {index + 2} | Status: '{status_atual}'")
        if status_atual != "PENDENTE":
            print("Ignorando registro...")
            continue

        print("Registro pendente encontrado. Iniciando preenchimento...")

        botao_popup = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".btn.btn-info.bootbox-accept")
            )
        )
        botao_popup.click()
        time.sleep(TEMPO_DE_ESPERA)

        driver.get(f"{URL_SISTEMA.rstrip('/')}/Scheduling/Import")
        time.sleep(TEMPO_DE_ESPERA)

        botao_popup = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".btn.btn-info.bootbox-accept")
            )
        )
        botao_popup.click()
        time.sleep(TEMPO_DE_ESPERA)

        container = str(linha.get("CONTAINER", "")).strip()
        armador = str(linha.get("ARMADOR", "")).strip()
        tipo = str(linha.get("TAMANHO", "")).strip()
        cpf = str(linha.get("CPF", "")).strip()
        placa = str(linha.get("CAVALO", "")).strip()

        wait.until(EC.presence_of_element_located((By.ID, "UnitsBooking")))
        driver.find_element(By.ID, "UnitsBooking").send_keys(container)
        pyautogui.press("tab")

        try:
            mensagem_erro = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".alertify-logs .error")
                )
            )
            texto_erro = mensagem_erro.text
            print(f"Registro {container} ignorado: {texto_erro}")

            df.at[index, "STATUS"] = "ERRO - VALIDACAO"
            salvar_planilha(df)
            continue

        except TimeoutException:
            print("Validação concluída; continuando.")

        time.sleep(TEMPO_DE_ESPERA)

        elemento_armador = wait.until(
            EC.presence_of_element_located((By.ID, "Owner"))
        )
        Select(elemento_armador).select_by_visible_text(armador)

        time.sleep(TEMPO_DE_ESPERA)

        tipo_limpo = tipo.replace(" ", "").upper()
        elemento_tipo = wait.until(
            EC.presence_of_element_located((By.ID, "Type"))
        )
        dropdown_tipo = Select(elemento_tipo)

        opcao_encontrada = False
        for opcao in dropdown_tipo.options:
            texto_opcao_site = opcao.text.replace(" ", "").upper()
            if tipo_limpo == texto_opcao_site:
                dropdown_tipo.select_by_value(opcao.get_attribute("value"))
                opcao_encontrada = True
                break

        if not opcao_encontrada:
            print(f"Atenção: tipo '{tipo}' não encontrado.")
            df.at[index, "STATUS"] = "ERRO - TIPO NAO ENCONTRADO"
            salvar_planilha(df)
            continue

        time.sleep(TEMPO_DE_ESPERA)

        driver.find_element(By.ID, "CodImpExp").send_keys(CNPJ_FIXO)
        time.sleep(TEMPO_DE_ESPERA)

        driver.find_element(By.ID, "Ship").send_keys(NAVIO_FIXO)
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(TEMPO_DE_ESPERA)

        driver.find_element(By.ID, "Cpf").send_keys(cpf)
        time.sleep(TEMPO_DE_ESPERA)

        driver.find_element(By.ID, "Plate").send_keys(placa)
        time.sleep(TEMPO_DE_ESPERA)

        data_atual = datetime.now()
        data_alvo = data_atual + timedelta(days=20)

        if data_alvo.weekday() == 5:
            data_alvo += timedelta(days=2)
        elif data_alvo.weekday() == 6:
            data_alvo += timedelta(days=1)

        dia_alvo = str(data_alvo.day)

        if data_alvo.month != data_atual.month:
            print("Data no próximo mês; avançando o calendário.")
            dia_proximo_mes = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "td.new.day")
                )
            )
            dia_proximo_mes.click()
            time.sleep(1)

        print(f"Selecionando dia {dia_alvo}...")
        xpath_dia_alvo = (
            "//div[@class='datepicker-days']//td"
            "[contains(@class, 'day') "
            "and not(contains(@class, 'old')) "
            "and not(contains(@class, 'new')) "
            f"and text()='{dia_alvo}']"
        )

        botao_dia_alvo = wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath_dia_alvo))
        )
        botao_dia_alvo.click()
        time.sleep(2)

        horarios = driver.find_elements(
            By.CSS_SELECTOR, "#ScheduledTime tr.Hours"
        )

        horario_selecionado = False
        for horario in reversed(horarios):
            colunas = horario.find_elements(By.TAG_NAME, "td")
            if len(colunas) < 2:
                continue

            try:
                vagas = int(colunas[1].text.strip())
            except ValueError:
                continue

            if vagas > 0:
                horario.click()
                horario_selecionado = True
                break

        if not horario_selecionado:
            print("Nenhum horário disponível para este registro.")
            df.at[index, "STATUS"] = "ERRO - SEM HORARIO"
            salvar_planilha(df)
            continue

        driver.find_element(By.ID, "submit").click()

        df.at[index, "STATUS"] = "REALIZADO"
        salvar_planilha(df)

        time.sleep(3)

    print("Processamento concluído.")

finally:
    driver.quit()
