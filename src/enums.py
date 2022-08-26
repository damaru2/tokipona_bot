from enum import Enum


class Colors(Enum):
    pimeja="000000"
    jelo="FFFF00"
    loje="FF0000"
    loje_walo="FFCCCC"
    laso_kasi="00FF00"
    laso_kasi_walo="CCFFCC"
    laso_sewi="0000FF"
    laso_sewi_walo="CCCCFF"
    pimeja_walo_walo="AAAAAA"
    pimeja_walo="999999"
    pimeja_pimeja_walo="666666"
    pimeja_pimeja_pimeja_walo="333333"
    walo="FFFFFF"

class Selectable(Enum):
    change_font_type = "0"
    change_font_color = "1"
    change_background_color = "2"
    go_back = "-1"


class Fonts(Enum):
    # These are sitelen pona fonts
    linja_pona_jan_same="1"
    linja_leko_jan_selano="2"
    sitelen_luka_tu_tu_jan_inkepa="3"
    sitelen_pona_jan_wesi="4"
    linja_pimeja_jan_inkepa="10"
    linja_pi_tomo_lipu="12"
    sitelen_pi_linja_ko_jan_inkepa="13"
    sitelen_pona_pona_jan_jaku="14"
    insa_pi_supa_lape_int_main="15"
    linja_sike_jan_lipamanka="17"
    linja_suwi_anna="18"
    linja_pi_pu_lukin_jan_sa="19"

    # These are not sitelen pona fonts
    linja_kute_mute_jan_inkepa="5"
    linja_kute_mute_tu_jan_inkepa="6"
    linja_kute_mute_regular_jan_inkepa="7"
    linja_kama_wan_jan_inkepa="8"
    toki_tengwar_jan_pije="9"


fonts_dict = {
    Fonts.linja_pona_jan_same.value:                  "Linja Pona - jan Same",
    Fonts.linja_leko_jan_selano.value:                "Linja Leko - jan Selano",
    Fonts.sitelen_luka_tu_tu_jan_inkepa.value:        "Sitelen Luka 4 - jan Inkepa",
    Fonts.sitelen_pona_jan_wesi.value:                "Sitelen Pona - jan Wesi",
    Fonts.linja_pimeja_jan_inkepa.value:              "Linja Pimeja - jan Inkepa",
    Fonts.linja_pi_tomo_lipu.value:                   "linja pi tomo lipu",
    Fonts.sitelen_pi_linja_ko_jan_inkepa.value:       "Linja Ko - jan Inkepa",
    Fonts.sitelen_pona_pona_jan_jaku.value:           "Sitelen Pona Pona - jan Jaku",
    Fonts.insa_pi_supa_lape_int_main.value:           "Insa Pi Supa Lape - jan int main();",
    Fonts.linja_sike_jan_lipamanka.value:             "Linja Sike - jan Lipamanka",
    Fonts.linja_suwi_anna.value:                      "Linja Suwi - Anna",
    Fonts.linja_pi_pu_lukin_jan_sa.value:             "Linja pi pu lukin - jan Sa",
}

colors_dict = {
    Colors.pimeja.value: "pimeja",
    Colors.jelo.value: "jelo",
    Colors.loje.value: "loje",
    Colors.loje_walo.value: "loje walo",
    Colors.laso_kasi.value: "laso kasi",
    Colors.laso_kasi_walo.value: "laso kasi walo",
    Colors.laso_sewi.value: "laso sewi",
    Colors.laso_sewi_walo.value: "laso sewi walo",
    Colors.pimeja_walo_walo.value: "pimeja walo walo",
    Colors.pimeja_walo.value: "pimeja walo",
    Colors.pimeja_pimeja_walo.value: "pimeja pimeja walo",
    Colors.pimeja_pimeja_pimeja_walo.value: "pimeja pimeja pimeja walo",
    Colors.walo.value: "walo",
}


pu = ["a", "akesi", "alasa", "anpa", "ante", "awen", "ala", "ali", "ale", "anu", "e", "en", "esun", "insa", "ijo", "ike", "ilo", "jaki", "jelo", "jan", "jo", "kalama", "kulupu", "kiwen", "kala", "kama", "kasi", "ken", "kepeken", "kili", "kule", "kute", "kon", "ko", "linja", "lukin", "lape", "laso", "lawa", "lete", "lili", "lipu", "loje", "luka", "lupa", "len", "lon", "la", "li", "monsi", "mama", "mani", "meli", "mije", "moku", "moli", "musi", "mute", "mun", "ma", "mi", "mu", "nanpa", "nasin", "nasa", "nena", "nimi", "noka", "ni", "oo", "olin", "open", "ona", "pakala", "palisa", "pimeja", "pilin", "pali", "pana", "pini", "pipi", "poka", "poki", "pona", "pan", "pi", "pu", "sitelen", "sijelo", "sinpin", "soweli", "sama", "seli", "selo", "seme", "sewi", "sike", "sina", "sona", "suli", "suno", "supa", "suwi", "sin", "tenpo", "taso", "tawa", "telo", "toki", "tomo", "tan", "tu", "utala", "unpa", "uta", "walo", "waso", "wawa", "weka", "wile", "wan"]


ku_suli = ["epiku", "jasima", "kijetesantakalu", "kin", "kipisi", "kokosila", "ku", "lanpan", "leko", "meso", "misikeke", "monsuta", "n", "namako", "oko", "soko", "tonsi"]


ku_lili = ["apeja", "ete", "ewe", "isipin", "kalamARR", "kalamawala", "kan", "kapesi", "ke", "kese", "kiki", "kulijo", "kuntu", "likujo", "linluwi", "loka", "majuna", "misa", "mulapisu", "neja", "oke", "pake", "pata", "peto", "Pingo", "po", "polinpin", "pomotolo", "powe", "samu", "san", "soto", "sutopatikuna", "taki", "te", "teje", "to", "tuli", "umesu", "unu", "usawi", "waleja", "yupekosi"]

