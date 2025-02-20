import pytest
from bs4 import BeautifulSoup

HTML_FILE = "index.html"

@pytest.fixture
def html_content():
    """Beolvassa a HTML fájlt és BeautifulSoup objektummá alakítja."""
    with open(HTML_FILE, "r", encoding="utf-8") as file:
        return BeautifulSoup(file, "html.parser")

def get_style_rules(html_content):
    """Kinyeri a CSS szabályokat a <style> blokkból."""
    styles = {}
    style_tag = html_content.find("style")
    
    if style_tag:
        rules = style_tag.string.split("}")
        for rule in rules:
            parts = rule.strip().split("{")
            if len(parts) == 2:
                selector = parts[0].strip()
                declarations = parts[1].strip().split(";")
                styles[selector] = {decl.split(":")[0].strip(): decl.split(":")[1].strip() for decl in declarations if ":" in decl}
    
    return styles

@pytest.fixture
def css_rules(html_content):
    """Visszaadja a CSS szabályokat egy dictionary-ben."""
    return get_style_rules(html_content)

# === HTML TESZTEK ===

def test_container_exists(html_content):
    """Ellenőrzi, hogy a .container osztály létezik-e."""
    assert html_content.find("div", class_="container"), "A .container elem nem található!"

def test_h1_exists(html_content):
    """Ellenőrzi, hogy a .container tartalmaz-e h1 elemet."""
    container = html_content.find("div", class_="container")
    assert container and container.find("h1"), "A h1 elem nem található a .container-en belül!"

def test_h1_text(html_content):
    """Ellenőrzi, hogy a h1 elem szövege megfelelő-e."""
    h1 = html_content.find("div", class_="container").find("h1")
    assert "Lorem ipsum" in h1.text, "A h1 elem szövege nem megfelelő!"

def test_h3_exists(html_content):
    """Ellenőrzi, hogy a h3 alcím létezik-e."""
    assert html_content.find("h3"), "A h3 elem nem található!"

def test_h3_text(html_content):
    """Ellenőrzi, hogy a h3 elem szövege megfelelő-e."""
    h3 = html_content.find("h3")
    assert h3.text.strip() == "Dolor sit amet", "A h3 elem szövege nem megfelelő!"

def test_aside_exists(html_content):
    """Ellenőrzi, hogy az aside elem létezik-e."""
    assert html_content.find("aside"), "Az aside elem nem található!"

def test_aside_text_word_count(html_content):
    """Ellenőrzi, hogy az aside elem szövege pontosan 10 szóból áll-e."""
    aside = html_content.find("aside")
    words = aside.text.strip().split()
    assert len(words) == 10, "Az aside elem szövege nem 10 szóból áll!"

# === CSS TESZTEK ===

def test_container_styles(css_rules):
    """Ellenőrzi a .container stílusait."""
    assert ".container" in css_rules, "A .container osztály nem szerepel a CSS-ben!"
    styles = css_rules[".container"]
    
    assert styles.get("margin") == "5%", "A .container margója nem megfelelő!"
    assert styles.get("background-color") == "cyan", "A .container háttérszíne nem cyan!"
    assert styles.get("padding") == "15px", "A .container belső margója nem megfelelő!"

def test_aside_styles(css_rules):
    """Ellenőrzi az aside stílusait."""
    assert "aside" in css_rules, "Az aside elem nem szerepel a CSS-ben!"
    styles = css_rules["aside"]
    
    assert styles.get("width") == "95px", "Az aside szélessége nem megfelelő!"
    assert styles.get("height") == "95px", "Az aside magassága nem megfelelő!"
    assert styles.get("font-size") == "14px", "Az aside fontmérete nem megfelelő!"
    assert styles.get("background-color") == "white", "Az aside háttérszíne nem fehér!"
    assert styles.get("padding") == "10px", "Az aside belső margója nem megfelelő!"
    assert styles.get("float") == "left", "Az aside nem lebeg balra!"
    assert styles.get("margin-right") == "10px", "Az aside jobboldali margója nem megfelelő!"
    assert styles.get("border-right") == "6px solid goldenrod", "Az aside jobb szegélye nem megfelelő!"

def test_last_paragraph_third_word_bold(html_content):
    """Ellenőrzi, hogy az utolsó <p> elem harmadik szava félkövér-e."""
    paragraphs = html_content.find_all("p")
    assert paragraphs, "Nem található <p> elem!"
    
    last_p = paragraphs[-1]
    words = last_p.text.strip().split()
    
    bold_words = [b.text for b in last_p.find_all("b")]
    
    assert len(words) >= 3, "A bekezdésnek legalább 3 szóból kell állnia!"
    assert words[2] in bold_words, "A harmadik szó nem félkövér!"
