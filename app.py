import math
import random
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="TOX-LAB | Simulador de Toxicología",
    page_icon="🧪",
    layout="wide",
)

# ----------------------------
# Estilo
# ----------------------------
st.markdown(
    """
    <style>
    .main-title {font-size: 2.6rem; font-weight: 800; margin-bottom: .2rem;}
    .subtitle {font-size: 1.1rem; color: #555; margin-bottom: 1.4rem;}
    .case-box {padding: 1rem 1.2rem; border: 1px solid #ddd; border-radius: 14px; background: #fafafa;}
    .concept-box {padding: .8rem 1rem; border-left: 5px solid #777; background: #f6f6f6; margin: .7rem 0 1rem 0;}
    .small-note {font-size: .88rem; color: #666;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Estado
# ----------------------------
DEFAULTS = {
    "started": False,
    "student": "",
    "level": 1,
    "score": 0,
    "answered": {},
    "feedback": {},
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

TOTAL_LEVELS = 8
MAX_POINTS = 100


def reset_game():
    for key, value in DEFAULTS.items():
        st.session_state[key] = value.copy() if isinstance(value, dict) else value
    st.rerun()


def mark_answer(level, correct, points, explanation):
    if not st.session_state.answered.get(level, False):
        st.session_state.answered[level] = True
        if correct:
            st.session_state.score += points
        st.session_state.feedback[level] = (correct, explanation)


def show_feedback(level):
    if level in st.session_state.feedback:
        correct, explanation = st.session_state.feedback[level]
        if correct:
            st.success(f"✅ Correcto. {explanation}")
        else:
            st.error(f"❌ Revisa el razonamiento. {explanation}")


def next_level():
    if st.session_state.level < TOTAL_LEVELS:
        st.session_state.level += 1
        st.rerun()


def previous_level():
    if st.session_state.level > 1:
        st.session_state.level -= 1
        st.rerun()


def navigation():
    c1, c2, c3 = st.columns([1, 1, 4])
    with c1:
        st.button("← Anterior", on_click=previous_level, disabled=st.session_state.level == 1)
    with c2:
        st.button(
            "Siguiente →",
            on_click=next_level,
            disabled=not st.session_state.answered.get(st.session_state.level, False) or st.session_state.level == TOTAL_LEVELS,
        )


def dose_response_plot():
    doses = [0, 1, 2, 4, 8, 16, 32, 64]
    responses = [100 / (1 + math.exp(-0.18 * (d - 18))) for d in doses]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(doses, responses, marker="o")
    ax.axhline(50, linestyle="--", linewidth=1)
    ax.set_xlabel("Dosis (mg/kg)")
    ax.set_ylabel("Respuesta (%)")
    ax.set_title("Curva dosis–respuesta hipotética")
    ax.set_ylim(0, 105)
    ax.grid(alpha=0.2)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# ----------------------------
# Pantalla de inicio
# ----------------------------
if not st.session_state.started:
    st.markdown('<div class="main-title">🧪 TOX-LAB</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Simulador interactivo de conceptos fundamentales de Toxicología</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="case-box">
        <b>Misión:</b> resolver una serie de desafíos toxicológicos aplicando dosis, exposición,
        biodisponibilidad, relación dosis–respuesta, DL₅₀, NOAEL, LOAEL y evaluación integrada del riesgo.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    student = st.text_input("Nombre del estudiante o equipo")
    st.caption("La puntuación máxima es de 100 puntos. Cada nivel se responde una sola vez.")
    if st.button("Iniciar misión", type="primary", use_container_width=True):
        if student.strip():
            st.session_state.student = student.strip()
            st.session_state.started = True
            st.rerun()
        else:
            st.warning("Escriba un nombre para iniciar.")
    st.stop()

# ----------------------------
# Encabezado general
# ----------------------------
st.markdown('<div class="main-title">🧪 TOX-LAB</div>', unsafe_allow_html=True)
st.caption(f"Participante: {st.session_state.student}")

p1, p2, p3 = st.columns([5, 1, 1])
with p1:
    st.progress(st.session_state.level / TOTAL_LEVELS, text=f"Nivel {st.session_state.level} de {TOTAL_LEVELS}")
with p2:
    st.metric("Puntaje", f"{st.session_state.score}/{MAX_POINTS}")
with p3:
    st.button("Reiniciar", on_click=reset_game)

st.divider()
level = st.session_state.level

# ----------------------------
# Nivel 1
# ----------------------------
if level == 1:
    st.header("Nivel 1 · La dosis hace al veneno")
    st.markdown('<div class="concept-box"><b>Concepto:</b> La dosis relaciona la cantidad de sustancia con el peso corporal del individuo expuesto.</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="case-box">
        Un perro de <b>12 kg</b> ingiere accidentalmente <b>60 mg</b> de una sustancia.
        ¿Cuál fue la dosis administrada en mg/kg?
        </div>
        """,
        unsafe_allow_html=True,
    )
    answer = st.number_input("Dosis (mg/kg)", min_value=0.0, step=0.1, key="q1")
    if st.button("Comprobar", key="check1", disabled=st.session_state.answered.get(1, False)):
        correct = math.isclose(answer, 5.0, rel_tol=0, abs_tol=0.05)
        mark_answer(1, correct, 10, "60 mg ÷ 12 kg = 5 mg/kg. Expresar la dosis por kg permite comparar exposiciones entre individuos de diferente peso.")
    show_feedback(1)
    navigation()

# ----------------------------
# Nivel 2
# ----------------------------
elif level == 2:
    st.header("Nivel 2 · Biodisponibilidad")
    st.markdown('<div class="concept-box"><b>Concepto:</b> La biodisponibilidad (F) es la fracción de la dosis administrada que alcanza la circulación sistémica sin cambios.</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="case-box">
        Un animal recibe <b>10 mg/kg por vía oral</b>. La biodisponibilidad es de <b>40 %</b>.
        ¿Qué cantidad de la dosis, expresada en mg/kg, alcanza sistémicamente la circulación?
        </div>
        """,
        unsafe_allow_html=True,
    )
    answer = st.number_input("Dosis sistémicamente disponible (mg/kg)", min_value=0.0, step=0.1, key="q2")
    if st.button("Comprobar", key="check2", disabled=st.session_state.answered.get(2, False)):
        correct = math.isclose(answer, 4.0, rel_tol=0, abs_tol=0.05)
        mark_answer(2, correct, 12, "10 mg/kg × 0,40 = 4 mg/kg. La dosis administrada no necesariamente equivale a la dosis que llega a circulación sistémica.")
    show_feedback(2)
    navigation()

# ----------------------------
# Nivel 3
# ----------------------------
elif level == 3:
    st.header("Nivel 3 · Exposición, peligro y riesgo")
    st.markdown(
        """
        <div class="case-box">
        Un producto tiene toxicidad intrínseca elevada, pero permanece almacenado en un recipiente cerrado,
        fuera del alcance de animales y personas. ¿Cuál afirmación es la más correcta?
        </div>
        """,
        unsafe_allow_html=True,
    )
    options = [
        "Como es peligroso, el riesgo necesariamente es alto.",
        "Puede existir un peligro elevado, pero el riesgo depende también de la probabilidad y magnitud de exposición.",
        "Si no hay exposición, la sustancia deja de ser peligrosa.",
        "Peligro y riesgo son sinónimos.",
    ]
    answer = st.radio("Seleccione una opción", options, index=None, key="q3")
    if st.button("Comprobar", key="check3", disabled=st.session_state.answered.get(3, False)):
        correct = answer == options[1]
        mark_answer(3, correct, 10, "El peligro describe la capacidad intrínseca de causar daño; el riesgo incorpora la exposición y la probabilidad de que ese daño ocurra.")
    show_feedback(3)
    navigation()

# ----------------------------
# Nivel 4
# ----------------------------
elif level == 4:
    st.header("Nivel 4 · Interpretación de la DL₅₀")
    data = pd.DataFrame(
        {
            "Sustancia": ["A", "B", "C"],
            "DL₅₀ oral (mg/kg)": [5, 50, 500],
        }
    )
    st.dataframe(data, hide_index=True, use_container_width=True)
    answer = st.radio(
        "¿Cuál presenta mayor toxicidad aguda bajo estas condiciones experimentales?",
        ["Sustancia A", "Sustancia B", "Sustancia C", "Las tres son iguales"],
        index=None,
        key="q4",
    )
    if st.button("Comprobar", key="check4", disabled=st.session_state.answered.get(4, False)):
        correct = answer == "Sustancia A"
        mark_answer(4, correct, 14, "Una DL₅₀ menor indica que se necesita una dosis menor para producir mortalidad en el 50 % de la población experimental. No debe interpretarse como una frontera absoluta entre dosis segura y tóxica.")
    show_feedback(4)
    navigation()

# ----------------------------
# Nivel 5
# ----------------------------
elif level == 5:
    st.header("Nivel 5 · Curva dosis–respuesta")
    dose_response_plot()
    answer = st.select_slider(
        "A partir de la gráfica, ¿en qué intervalo se encuentra aproximadamente la dosis que produce una respuesta del 50 %?",
        options=["0–5 mg/kg", "5–10 mg/kg", "10–20 mg/kg", "20–40 mg/kg", ">40 mg/kg"],
        key="q5",
    )
    if st.button("Comprobar", key="check5", disabled=st.session_state.answered.get(5, False)):
        correct = answer == "10–20 mg/kg"
        mark_answer(5, correct, 12, "La respuesta del 50 % se alcanza aproximadamente alrededor de 18 mg/kg en esta curva hipotética. La posición de la curva ayuda a interpretar potencia y sensibilidad de la población.")
    show_feedback(5)
    navigation()

# ----------------------------
# Nivel 6
# ----------------------------
elif level == 6:
    st.header("Nivel 6 · NOAEL y LOAEL")
    data = pd.DataFrame(
        {
            "Dosis (mg/kg)": [0, 1, 5, 10, 25, 50],
            "Hallazgo": [
                "Sin efecto adverso observado",
                "Sin efecto adverso observado",
                "Sin efecto adverso observado",
                "Elevación adversa de ALT",
                "Lesión hepática",
                "Necrosis hepática",
            ],
        }
    )
    st.dataframe(data, hide_index=True, use_container_width=True)
    c1, c2 = st.columns(2)
    with c1:
        noael = st.selectbox("NOAEL", [0, 1, 5, 10, 25, 50], index=None, key="q6a")
    with c2:
        loael = st.selectbox("LOAEL", [0, 1, 5, 10, 25, 50], index=None, key="q6b")
    if st.button("Comprobar", key="check6", disabled=st.session_state.answered.get(6, False)):
        correct = noael == 5 and loael == 10
        mark_answer(6, correct, 14, "NOAEL = 5 mg/kg, la dosis más alta sin efecto adverso observado; LOAEL = 10 mg/kg, la dosis más baja en la que aparece un efecto adverso observado.")
    show_feedback(6)
    navigation()

# ----------------------------
# Nivel 7
# ----------------------------
elif level == 7:
    st.header("Nivel 7 · Comparación de exposiciones")
    st.markdown("Todos los animales ingirieron **40 mg** del mismo compuesto. Calcule la dosis oral por kg y considere la biodisponibilidad.")
    animals = pd.DataFrame(
        {
            "Animal": ["A", "B", "C", "D"],
            "Peso (kg)": [10, 5, 10, 20],
            "Cantidad ingerida (mg)": [40, 40, 40, 40],
            "Biodisponibilidad": ["70 %", "70 %", "90 %", "30 %"],
            "Condición": ["Adulto sano", "Adulto sano", "Enfermedad hepática", "Adulto sano"],
        }
    )
    st.dataframe(animals, hide_index=True, use_container_width=True)
    answer = st.radio(
        "Considerando solo dosis por kg y biodisponibilidad, ¿cuál presenta la mayor dosis sistémicamente disponible?",
        ["Animal A", "Animal B", "Animal C", "Animal D"],
        index=None,
        key="q7",
    )
    if st.button("Comprobar", key="check7", disabled=st.session_state.answered.get(7, False)):
        # A: 4*0.7=2.8; B:8*0.7=5.6; C:4*0.9=3.6; D:2*0.3=.6
        correct = answer == "Animal B"
        mark_answer(7, correct, 14, "B recibe 40/5 = 8 mg/kg; con F = 0,70, la dosis sistémicamente disponible es 5,6 mg/kg. Esto no significa que la biodisponibilidad sea el único determinante de toxicidad clínica.")
    show_feedback(7)
    navigation()

# ----------------------------
# Nivel 8
# ----------------------------
elif level == 8:
    st.header("Nivel 8 · Caso integrador")
    st.markdown(
        """
        <div class="case-box">
        Un tóxico experimental tiene una <b>DL₅₀ oral de 25 mg/kg</b>. Un perro de 10 kg ingiere 100 mg.
        La biodisponibilidad oral estimada es 60 %. El animal además presenta una alteración que reduce la eliminación del compuesto.
        ¿Cuál interpretación integra mejor los datos disponibles?
        </div>
        """,
        unsafe_allow_html=True,
    )
    options = [
        "La dosis es 10 mg/kg; como está por debajo de la DL₅₀, se puede afirmar que es segura.",
        "La dosis es 10 mg/kg y la dosis sistémicamente disponible estimada es 6 mg/kg; aun así, no puede descartarse toxicidad porque la DL₅₀ no define un umbral de seguridad y una eliminación reducida puede aumentar la exposición interna.",
        "La biodisponibilidad de 60 % significa que el 60 % del animal desarrollará signos clínicos.",
        "La alteración de la eliminación no modifica la exposición porque la dosis administrada ya está definida.",
    ]
    answer = st.radio("Seleccione la interpretación más sólida", options, index=None, key="q8")
    if st.button("Finalizar misión", key="check8", disabled=st.session_state.answered.get(8, False)):
        correct = answer == options[1]
        mark_answer(8, correct, 14, "La evaluación toxicológica integra dosis externa, biodisponibilidad y toxicocinética. La DL₅₀ caracteriza mortalidad aguda bajo condiciones específicas y no constituye por sí misma un límite individual de seguridad.")
        st.rerun()

    show_feedback(8)

    if st.session_state.answered.get(8, False):
        st.divider()
        score = st.session_state.score
        pct = score
        if pct >= 90:
            level_name = "Dominio sobresaliente"
            msg = "Integra con solidez los conceptos cuantitativos y de evaluación del riesgo."
        elif pct >= 75:
            level_name = "Buen dominio"
            msg = "La base conceptual es sólida; conviene revisar los niveles en los que hubo errores."
        elif pct >= 60:
            level_name = "Dominio en desarrollo"
            msg = "Reconoce varios conceptos, pero necesita reforzar su interpretación integrada."
        else:
            level_name = "Requiere refuerzo"
            msg = "Conviene revisar dosis, biodisponibilidad, DL₅₀ y NOAEL/LOAEL antes de repetir el desafío."

        st.subheader("Resultado final")
        r1, r2 = st.columns(2)
        with r1:
            st.metric("Puntuación", f"{score}/100")
        with r2:
            st.metric("Nivel alcanzado", level_name)
        st.info(msg)

        st.markdown("#### Revisión por nivel")
        rows = []
        titles = {
            1: "Dosis",
            2: "Biodisponibilidad",
            3: "Peligro y riesgo",
            4: "DL₅₀",
            5: "Dosis–respuesta",
            6: "NOAEL / LOAEL",
            7: "Exposición integrada",
            8: "Caso final",
        }
        for i in range(1, 9):
            ok, _ = st.session_state.feedback.get(i, (False, ""))
            rows.append({"Nivel": i, "Concepto": titles[i], "Resultado": "Correcto" if ok else "Revisar"})
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        st.button("Intentar nuevamente", on_click=reset_game, type="primary")

st.divider()
st.caption("TOX-LAB · Actividad educativa. Los valores y escenarios se presentan con fines pedagógicos y no sustituyen una evaluación clínica o regulatoria real.")
