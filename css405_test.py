import pytest
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

HTML_FILE = "index.html"
CSS_FILE = "style.css"

@pytest.fixture
def html_content():
    """Beolvassa a HTML fájlt és BeautifulSoup objektummá alakítja."""
    with open(HTML_FILE, "r", encoding="utf-8") as file:
        return BeautifulSoup(file, "html.parser")

def test_container_exists(html_content):
    """Ellenőrzi, hogy a .container osztály létezik-e."""
    assert html_content.find("div", class_="container"), "A .container elem nem található!"

def test_h1_inside_container(html_content):
    """Ellenőrzi, hogy a h1 cím létezik-e a .container-ben."""
    container = html_content.find("div", class_="container")
    h1 = container.find("h1")
    assert h1, "A h1 elem nem található a .container-en belül!"
    assert "Lorem ipsum" in h1.text, "A h1 elem szövege nem megfelelő!"

def test_h3_exists(html_content):
    """Ellenőrzi, hogy a h3 alcím létezik-e és megfelelő-e a szövege."""
    h3 = html_content.find("h3")
    assert h3, "A h3 elem nem található!"
    assert h3.text.strip() == "Dolor sit amet", "A h3 elem szövege nem megfelelő!"

def test_aside_exists(html_content):
    """Ellenőrzi, hogy az aside elem létezik-e és tartalmaz 10 szavas Lorem Ipsum szöveget."""
    aside = html_content.find("aside")
    assert aside, "Az aside elem nem található!"
    words = aside.text.strip().split()
    assert len(words) == 10, "Az aside elem szövege nem 10 szóból áll!"

@pytest.fixture(scope="module")
def browser():
    """Inicializálja a Selenium WebDriver-t."""
    options = Options()
    options.add_argument("--headless")
    service = Service("chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{HTML_FILE}")
    yield driver
    driver.quit()

def test_container_styles(browser):
    """Ellenőrzi a .container stílusait."""
    container = browser.find_element(By.CLASS_NAME, "container")
    assert container.value_of_css_property("margin") == "5%", "A .container margója nem megfelelő!"
    assert container.value_of_css_property("background-color") == "rgba(0, 255, 255, 1)", "A .container háttérszíne nem cyan!"
    assert container.value_of_css_property("padding") == "15px", "A .container belső margója nem megfelelő!"

def test_aside_styles(browser):
    """Ellenőrzi az aside stílusait."""
    aside = browser.find_element(By.TAG_NAME, "aside")
    assert aside.value_of_css_property("width") == "95px", "Az aside szélessége nem megfelelő!"
    assert aside.value_of_css_property("height") == "95px", "Az aside magassága nem megfelelő!"
    assert aside.value_of_css_property("font-size") == "14px", "Az aside fontmérete nem megfelelő!"
    assert aside.value_of_css_property("background-color") == "rgba(255, 255, 255, 1)", "Az aside háttérszíne nem fehér!"
    assert aside.value_of_css_property("padding") == "10px", "Az aside belső margója nem megfelelő!"
    assert aside.value_of_css_property("float") == "left", "Az aside nem lebeg balra!"
    assert aside.value_of_css_property("margin-right") == "10px", "Az aside jobboldali margója nem megfelelő!"
    assert aside.value_of_css_property("border-right") == "6px solid goldenrod", "Az aside jobb szegélye nem megfelelő!"

def test_last_paragraph_third_word_bold(browser):
    """Ellenőrzi, hogy az utolsó p elem harmadik szava félkövér-e."""
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    last_p = paragraphs[-1]
    words = last_p.find_elements(By.TAG_NAME, "b")
    assert any(word.text == "dolor" for word in words), "A harmadik szó nem félkövér!"
 