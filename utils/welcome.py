
import streamlit.components.v1 as c

CCBOT = '''

 ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░▒▓████████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
 ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░  ░▒▓█▓▒░     
                                                                  
'''


# @st.cache(show_spinner=False, suppress_st_warning=True,ttl=600)
def robo_avatar_component():
    robo_html = "<div style='display: flex; flex-wrap: wrap; justify-content: left;'>"
    robo_avatar_seed = [0, 'aRoN', 'gptLAb', 180, 'nORa', 'dAVe', 'Julia', 'WEldO', 60]

    for i in range(1, 10):
        avatar_url = "https://api.dicebear.com/5.x/bottts-neutral/svg?seed={0}".format(
            robo_avatar_seed[i - 1])  # format((i)*r.randint(0,888))
        robo_html += "<img src='{0}' style='width: {1}px; height: {1}px; margin: 10px;'>".format(avatar_url, 50)
    robo_html += "</div>"

    robo_html = """<style>
          @media (max-width: 800px) {
            img {
              max-width: calc((100% - 60px) / 6);
              height: auto;
              margin: 0 10px 10px 0;
            }
          }
        </style>""" + robo_html

    c.html(robo_html, height=70)