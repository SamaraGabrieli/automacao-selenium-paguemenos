from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

espera = WebDriverWait(driver, 10)

driver.get("https://www.paguemenos.com.br/")

driver.maximize_window()


# =========================
# FUNÇÕES AUXILIARES
# =========================

def voltar_home():
    driver.get("https://www.paguemenos.com.br/")

    espera.until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                ".paguemenos-store-theme-9-x-inputNovaBusca"
            )
        )
    )


def pesquisa(produto):

    campo = espera.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".paguemenos-store-theme-9-x-inputNovaBusca")
        )
    )

    campo.send_keys(Keys.CONTROL, "a")
    campo.send_keys(Keys.BACKSPACE)

    campo.send_keys(produto)
    campo.send_keys(Keys.ENTER)


def selecionar_categoria(nome_categoria):

    categoria = espera.until(
        EC.element_to_be_clickable(
            (By.XPATH, f'//a[contains(.,"{nome_categoria}")]')
        )
    )

    categoria.click()


# =========================
# TESTES
# =========================

#Testando campo de pesquisa
def teste_pesquisa():

    pesquisa("dipirona")
    time.sleep(5)

    pesquisa("Protetor facial principia")
    time.sleep(5)

    pesquisa("fralda pampers")
    time.sleep(5)

#Testando ordenação
def teste_ordenacao():

    # abre opções de ordenação
    ordenar = espera.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                ".paguemenos-store-theme-9-x-containerOrdenarDesk"
            )
        )
    )

    driver.execute_script("arguments[0].click();", ordenar)

    time.sleep(2)

    # seleciona "Menor preço"
    menor_preco = espera.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//div[contains(text(),'Menor preço')]"
            )
        )
    )

    driver.execute_script("arguments[0].click();", menor_preco)

    time.sleep(5)

    print("Ordenação aplicada com sucesso")


#Testando pesquisa sem resultado
def teste_pesquisa_erro():

    pesquisa("asdfghghjkiottvb")

    espera.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//*[contains(text(),'Nenhum resultado')]"
            )
        )
    )

#Acessando as categorias
def teste_categoria():

    time.sleep(5)
    voltar_home()

    selecionar_categoria("Mamães e bebês")
    time.sleep(3)
    driver.back()


    selecionar_categoria("Medicamentos e Saúde")
    time.sleep(3)
    driver.back()

# Validação de inconsistência na quantidade de produtos
def teste_carrinho_quantidade():

    pesquisa("carmed")
    time.sleep(5)

    produtos = espera.until(
        EC.presence_of_all_elements_located(
            (
                By.CSS_SELECTOR,
                ".paguemenos-store-theme-9-x-productName"
            )
        )
    )

    produtos[0].click()

    time.sleep(5)

    mais = espera.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                ".vtex-numeric-stepper__plus-button"
            )
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        mais
    )

    time.sleep(2)

    # Já começa em 1
    # Então precisamos clicar 29 vezes

    for i in range(29):

        driver.execute_script(
            "arguments[0].click();",
            mais
        )

        time.sleep(0.1)

    botao = espera.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                ".vtex-add-to-cart-button-0-x-buttonText"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        botao
    )

    time.sleep(5)

    carrinho = espera.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                ".vtex-minicart-2-x-minicartIconContainer"
            )
        )
    )

    driver.execute_script("arguments[0].click();", carrinho)
    time.sleep(5)


#INCLUINDO PRODUTOS NO CARRINHO
def teste_carrinho():

    pesquisa("ibuprofeno")
    time.sleep(5)

    produtos = espera.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".paguemenos-store-theme-9-x-productName")
        )
    )

    produtos[0].click()

    time.sleep(3)

    botao = espera.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                ".vtex-add-to-cart-button-0-x-buttonText"
            )
        )
    )

    driver.execute_script("arguments[0].click();", botao)
    time.sleep(5)

    driver.back()
    time.sleep(3)

    produtos = espera.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".paguemenos-store-theme-9-x-productName")
        )
    )

    produtos[1].click()

    time.sleep(3)

    botao = espera.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                ".vtex-add-to-cart-button-0-x-buttonText"
            )
        )
    )

    driver.execute_script("arguments[0].click();", botao)
    time.sleep(5)

    carrinho = espera.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                ".vtex-minicart-2-x-minicartIconContainer"
            )
        )
    )

    driver.execute_script("arguments[0].click();", carrinho)
    time.sleep(5)


# Excluindo Produto do carrinho

def remove_produto():

    remove = espera.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             ".paguemenos-minicart-components-0-x-remove-item-button")
        )
    )
    driver.execute_script("arguments[0].click();", remove)
    time.sleep(5)

    confirmar = espera.until(
        EC.element_to_be_clickable(
            (By.ID, "AT-minicart-remove-confirm")
        )
    )

    driver.execute_script("arguments[0].click();", confirmar)

#CADASTRANDO CEP
def cadastrar_cep():

    continuar = espera.until(
        EC.element_to_be_clickable(
            (By.ID, "proceed-to-checkout")
        )
    )

    driver.execute_script("arguments[0].click();", continuar)

    time.sleep(5)

    cep = espera.until(
        EC.presence_of_element_located(
        (By.ID, "ship-postalCode")
        )
    )

    codigo_cep = "17026842"

    for numero in codigo_cep:
        cep.send_keys(numero)
        time.sleep(0.2)



# EXECUÇÃO DOS TESTES

teste_pesquisa()

teste_ordenacao()

teste_pesquisa_erro()

teste_categoria()

teste_carrinho_quantidade()

teste_carrinho()

remove_produto()

cadastrar_cep()




input("Pressione ENTER para sair...")

driver.quit()