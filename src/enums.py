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
    sitelen_pi_linja_ko_jan_inkepa="13"
    sitelen_pona_pona_jan_jaku="14"
    insa_pi_supa_lape_int_main="15"

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
    Fonts.sitelen_pi_linja_ko_jan_inkepa.value:       "Linja Ko - jan Inkepa",
    Fonts.sitelen_pona_pona_jan_jaku.value:           "Sitelen Pona Pona - jan Jaku",
    Fonts.insa_pi_supa_lape_int_main.value:           "Insa Pi Supa Lape - jan int main();",
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
