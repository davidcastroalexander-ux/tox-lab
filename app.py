import math
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='TOX-LAB 2.0 | Toxicología', page_icon='🧪', layout='wide')

st.markdown('''
<style>
.block-container{padding-top:2rem;max-width:1400px}.hero{padding:1.45rem 1.7rem;border:1px solid #dbe4f0;border-radius:18px;background:linear-gradient(135deg,#fff,#f4f8fd);margin-bottom:1rem}.hero h1{color:#102b5c;margin:0;font-size:2.7rem}.hero p{font-size:1.08rem;margin:.35rem 0 0;color:#40516c}.mission{padding:1rem 1.2rem;border:1px solid #d8e1ed;border-radius:14px;background:#fff;margin:.6rem 0 1rem}.concept{padding:.85rem 1rem;border-left:5px solid #163d77;background:#f4f7fb;border-radius:8px;margin:.6rem 0 1rem}.takehome{padding:.85rem 1rem;border:1px solid #e6d39a;background:#fffaf0;border-radius:12px}.flow{padding:.85rem;text-align:center;border-radius:12px;background:#eef4fb;color:#153a70;font-weight:700}.badge{display:inline-block;padding:.25rem .65rem;border-radius:999px;background:#eaf1fb;color:#173e78;font-weight:700;font-size:.85rem}.small{color:#667085;font-size:.9rem}
</style>''', unsafe_allow_html=True)

DEFAULTS={'started':False,'student':'','level':1,'score':0,'attempts':{},'solved':{},'feedback':{}}
for k,v in DEFAULTS.items():
    if k not in st.session_state: st.session_state[k]=v.copy() if isinstance(v,dict) else v

TOTAL=12
POINTS={1:8,2:8,3:8,4:8,5:8,6:8,7:8,8:9,9:9,10:9,11:8,12:9}
MODULES={1:'I · Exposición y dosis',2:'I · Exposición y dosis',3:'I · Exposición y dosis',4:'II · Toxicocinética',5:'II · Toxicocinética',6:'II · Toxicocinética',7:'II · Toxicocinética',8:'III · Toxicidad',9:'III · Toxicidad',10:'III · Toxicidad',11:'IV · Integración',12:'IV · Integración'}
TITLES={1:'Peligro y riesgo',2:'Dosis',3:'Concentración',4:'Biodisponibilidad',5:'Vida media',6:'Volumen de distribución',7:'AUC y clearance',8:'Dosis–respuesta',9:'DL₅₀',10:'NOAEL y LOAEL',11:'Comparación de pacientes',12:'Código rojo · Caso final'}

GLOSSARY={
'Dosis (D)':'Cantidad de sustancia administrada o absorbida. En toxicología suele normalizarse por peso corporal (p. ej., mg/kg).',
'Concentración (Cₚ)':'Cantidad de sustancia presente en plasma en un momento específico.',
'Tiempo (t)':'Variable cronológica utilizada para describir los cambios toxicocinéticos.',
'Biodisponibilidad (F)':'Fracción de una dosis administrada que alcanza la circulación sistémica sin cambios.',
'Vida media (t½)':'Tiempo requerido para que la concentración o cantidad del compuesto disminuya aproximadamente 50 % durante la fase considerada.',
'Vd':'Volumen aparente que relaciona la cantidad de sustancia en el organismo con su concentración plasmática: Vd = A/Cₚ.',
'Vdss':'Volumen aparente de distribución estimado cuando se alcanza el estado estacionario de distribución.',
'AUC':'Área bajo la curva concentración–tiempo; representa una medida de la exposición sistémica total durante el intervalo evaluado.',
'Clearance (CL)':'Volumen aparente de plasma del cual el compuesto es eliminado por unidad de tiempo. Puede integrar eliminación renal y no renal.',
'NOAEL':'Mayor nivel de exposición ensayado en el que no se observan efectos adversos atribuibles al agente bajo las condiciones del estudio.',
'LOAEL':'Menor nivel de exposición ensayado en el que se observa un efecto adverso atribuible al agente bajo las condiciones del estudio.',
'DL₅₀':'Dosis letal mediana: dosis que produce mortalidad en 50 % de una población experimental bajo condiciones definidas.'}

def reset():
    for k,v in DEFAULTS.items(): st.session_state[k]=v.copy() if isinstance(v,dict) else v
    st.rerun()

def concept(names):
    with st.expander('📚 Consultar concepto', expanded=False):
        for n in names: st.markdown(f'**{n}:** {GLOSSARY[n]}')

def submit(level, correct, explanation, hint):
    if st.session_state.solved.get(level): return
    a=st.session_state.attempts.get(level,0)+1; st.session_state.attempts[level]=a
    if correct:
        factor=1 if a==1 else .7 if a==2 else .4
        earned=round(POINTS[level]*factor)
        st.session_state.score+=earned; st.session_state.solved[level]=True
        st.session_state.feedback[level]=('ok',f'{explanation}  **+{earned} puntos.**')
    else:
        st.session_state.feedback[level]=('bad', hint if a==1 else f'{hint} Revisa el concepto y vuelve a intentarlo.')

def feedback(level):
    if level in st.session_state.feedback:
        kind,text=st.session_state.feedback[level]
        (st.success if kind=='ok' else st.warning)(('✅ ' if kind=='ok' else '💡 ')+text)

def nav():
    c1,c2,_=st.columns([1,1,5])
    if c1.button('← Anterior',disabled=st.session_state.level==1): st.session_state.level-=1; st.rerun()
    if c2.button('Siguiente →',disabled=not st.session_state.solved.get(st.session_state.level) or st.session_state.level==TOTAL): st.session_state.level+=1; st.rerun()

def mission(text): st.markdown(f'<div class="mission"><b>🎯 Desafío:</b> {text}</div>',unsafe_allow_html=True)
def takehome(text): st.markdown(f'<div class="takehome"><b>⭐ Idea clave:</b> {text}</div>',unsafe_allow_html=True)

def curve_plot():
    doses=list(range(0,41,2)); responses=[100/(1+math.exp(-.28*(d-18))) for d in doses]
    fig,ax=plt.subplots(figsize=(7,3.6)); ax.plot(doses,responses,marker='o',markevery=3); ax.axhline(50,ls='--',lw=1); ax.axvline(18,ls='--',lw=1); ax.set(xlabel='Dosis (mg/kg)',ylabel='Respuesta (%)',title='Curva dosis–respuesta hipotética'); ax.set_ylim(0,105); ax.grid(alpha=.2); st.pyplot(fig,use_container_width=True); plt.close(fig)

def pk_plot():
    t=[0,1,2,3,4]; c=[100,50,25,12.5,6.25]
    fig,ax=plt.subplots(figsize=(7,3.4)); ax.plot(t,c,marker='o'); ax.set_xticks(t); ax.set(xlabel='Número de vidas medias',ylabel='Concentración relativa',title='Disminución exponencial ilustrativa'); ax.grid(alpha=.2); st.pyplot(fig,use_container_width=True); plt.close(fig)

if not st.session_state.started:
    st.markdown('<div class="hero"><h1>🧪 TOX-LAB 2.0</h1><p>Simulador universitario de conceptos fundamentales de Toxicología</p></div>',unsafe_allow_html=True)
    st.markdown('<div class="flow">EXPOSICIÓN → DOSIS → ADME → EXPOSICIÓN INTERNA → RESPUESTA → RIESGO</div>',unsafe_allow_html=True)
    st.write('')
    c1,c2,c3,c4=st.columns(4)
    for c,t,d in [(c1,'Módulo I','Exposición y dosis'),(c2,'Módulo II','Toxicocinética'),(c3,'Módulo III','Toxicidad'),(c4,'Módulo IV','Integración')]: c.markdown(f'**{t}**  \n{d}')
    st.info('**Misión:** resolver 12 desafíos aplicando razonamiento cuantitativo e interpretación toxicológica. Puedes consultar conceptos durante la actividad.')
    student=st.text_input('Nombre del estudiante o equipo')
    st.caption('Puntaje máximo: 100. Primer intento correcto = 100 % de los puntos; segundo = 70 %; tercero o posterior = 40 %.')
    if st.button('Iniciar misión',type='primary',use_container_width=True):
        if student.strip(): st.session_state.student=student.strip(); st.session_state.started=True; st.rerun()
        else: st.warning('Escriba un nombre para iniciar.')
    st.stop()

st.markdown('<div class="hero"><h1>🧪 TOX-LAB 2.0</h1><p>Del contacto con el tóxico a la interpretación del riesgo</p></div>',unsafe_allow_html=True)
st.caption(f'Participante: {st.session_state.student}')
c1,c2,c3=st.columns([5,1,1]); c1.progress(st.session_state.level/TOTAL,text=f'Misión {st.session_state.level} de {TOTAL} · {MODULES[st.session_state.level]}'); c2.metric('Puntaje',f'{st.session_state.score}/100'); c3.button('Reiniciar',on_click=reset)
st.markdown(f'<span class="badge">{MODULES[st.session_state.level]}</span>',unsafe_allow_html=True)
st.header(f'Misión {st.session_state.level} · {TITLES[st.session_state.level]}')
L=st.session_state.level

if L==1:
    mission('Un compuesto posee alta capacidad intrínseca de causar daño, pero permanece en un recipiente sellado y fuera del alcance de animales. ¿Cuál interpretación distingue correctamente peligro de riesgo?')
    concept([])
    opts=['El riesgo necesariamente es alto porque el peligro es alto.','El peligro puede ser alto, pero el riesgo depende también de la exposición.','Sin exposición, la sustancia deja de ser peligrosa.','Peligro y riesgo son sinónimos.']
    a=st.radio('Seleccione:',opts,index=None,key='q1')
    if st.button('Comprobar',key='b1'): submit(1,a==opts[1],'El peligro es una propiedad intrínseca; el riesgo integra la posibilidad de exposición y la probabilidad/magnitud del daño.','Pregunta guía: ¿una sustancia pierde su capacidad de causar daño solo porque nadie entra en contacto con ella?')
    feedback(1); takehome('Peligro describe lo que un agente puede hacer; riesgo considera si, cuánto y cómo ocurre la exposición.'); nav()
elif L==2:
    mission('Un perro de 12 kg ingiere 60 mg de un compuesto. Calcula la dosis administrada en mg/kg.')
    concept(['Dosis (D)'])
    a=st.number_input('Dosis (mg/kg)',min_value=0.0,step=.1,key='q2')
    if st.button('Comprobar',key='b2'): submit(2,math.isclose(a,5,abs_tol=.05),'60 mg ÷ 12 kg = **5 mg/kg**.','Divide la cantidad total ingerida entre el peso corporal.')
    feedback(2); takehome('Normalizar la cantidad por kg permite comparar exposiciones entre individuos de diferente tamaño.'); nav()
elif L==3:
    mission('Una muestra plasmática contiene 24 mg del compuesto distribuidos en 3 L de plasma. ¿Cuál es la concentración plasmática media en este ejemplo simplificado?')
    concept(['Concentración (Cₚ)','Tiempo (t)'])
    a=st.number_input('Cₚ (mg/L)',min_value=0.0,step=.1,key='q3')
    if st.button('Comprobar',key='b3'): submit(3,math.isclose(a,8,abs_tol=.05),'24 mg ÷ 3 L = **8 mg/L**.','Concentración = cantidad / volumen.')
    feedback(3); takehome('La concentración describe cuánto compuesto está presente en un volumen determinado y cambia a lo largo del tiempo.'); nav()
elif L==4:
    mission('Un animal recibe 10 mg/kg por vía oral y F = 40 %. ¿Qué cantidad de la dosis, expresada en mg/kg, alcanza la circulación sistémica sin cambios?')
    concept(['Biodisponibilidad (F)','Dosis (D)'])
    st.markdown('**10 mg/kg administrados → F = 0,40 → ? mg/kg sistémicamente disponibles**')
    st.progress(.40,text='40 % de biodisponibilidad')
    a=st.number_input('Dosis sistémicamente disponible (mg/kg)',min_value=0.0,step=.1,key='q4')
    if st.button('Comprobar',key='b4'): submit(4,math.isclose(a,4,abs_tol=.05),'10 × 0,40 = **4 mg/kg**.','Convierte 40 % a 0,40 y multiplícalo por la dosis administrada.')
    feedback(4); takehome('Dosis administrada y exposición sistémica no son necesariamente equivalentes.'); nav()
elif L==5:
    mission('Observa la disminución ilustrativa. Si la concentración inicial es 100 unidades y la vida media es 2 h, ¿cuánto queda aproximadamente después de 6 h?')
    concept(['Vida media (t½)','Concentración (Cₚ)','Tiempo (t)']); pk_plot()
    a=st.radio('Seleccione:', ['50','25','12,5','6,25'],index=None,key='q5')
    if st.button('Comprobar',key='b5'): submit(5,a=='12,5','6 h corresponden a 3 vidas medias: 100 → 50 → 25 → **12,5**.','Cuenta cuántos intervalos de 2 h caben en 6 h y reduce a la mitad en cada intervalo.')
    feedback(5); takehome('La vida media caracteriza la velocidad de descenso de la cantidad/concentración en una fase determinada; no es el tiempo para “absorber 50 %”.'); nav()
elif L==6:
    mission('Dos compuestos tienen la misma cantidad corporal (100 mg). A presenta Cₚ = 20 mg/L y B Cₚ = 2 mg/L. Usando Vd = A/Cₚ, ¿cuál presenta mayor Vd?')
    concept(['Vd','Vdss','Concentración (Cₚ)'])
    df=pd.DataFrame({'Compuesto':['A','B'],'Cantidad corporal (mg)':[100,100],'Cₚ (mg/L)':[20,2]}); st.dataframe(df,hide_index=True,use_container_width=True)
    a=st.radio('Mayor Vd:', ['A','B','Son iguales'],index=None,key='q6')
    if st.button('Comprobar',key='b6'): submit(6,a=='B','A: 100/20 = 5 L; B: 100/2 = **50 L**. Un Vd mayor indica una menor concentración plasmática relativa a la cantidad corporal.','Calcula A/Cₚ para cada compuesto.')
    feedback(6); takehome('Vd es un volumen **aparente**: ayuda a describir la extensión de distribución, no un compartimento anatómico real.'); nav()
elif L==7:
    mission('Interpreta AUC y clearance. Si dos animales reciben una exposición comparable pero uno presenta menor clearance, ¿qué consecuencia es más probable, manteniendo constantes los demás factores?')
    concept(['AUC','Clearance (CL)'])
    opts=['Menor exposición sistémica y menor AUC.','Mayor persistencia y, en general, mayor exposición/AUC.','La eliminación no afecta la exposición.','La biodisponibilidad necesariamente se vuelve 100 %.']
    a=st.radio('Seleccione:',opts,index=None,key='q7')
    if st.button('Comprobar',key='b7'): submit(7,a==opts[1],'Una reducción del clearance puede prolongar la permanencia del compuesto y aumentar la exposición sistémica, reflejada en el AUC.','Clearance describe qué tan eficientemente el organismo elimina el compuesto por unidad de tiempo.')
    feedback(7); takehome('El clearance total puede integrar vías renales y no renales; AUC resume exposición sistémica a lo largo del tiempo.'); nav()
elif L==8:
    mission('Usa la curva para estimar la dosis que produce aproximadamente 50 % de respuesta.')
    curve_plot(); concept([])
    a=st.select_slider('Intervalo:',options=['0–5 mg/kg','5–10 mg/kg','10–20 mg/kg','20–40 mg/kg','>40 mg/kg'],key='q8')
    if st.button('Comprobar',key='b8'): submit(8,a=='10–20 mg/kg','La respuesta del 50 % se sitúa alrededor de **18 mg/kg** en esta curva hipotética.','Busca la intersección entre la línea horizontal de 50 % y la curva.')
    feedback(8); takehome('La relación dosis–respuesta permite caracterizar cómo cambia la magnitud o frecuencia de respuesta al variar la dosis.'); nav()
elif L==9:
    mission('Compara la toxicidad aguda de tres sustancias bajo las mismas condiciones experimentales.')
    concept(['DL₅₀']); st.dataframe(pd.DataFrame({'Sustancia':['A','B','C'],'DL₅₀ oral (mg/kg)':[5,50,500]}),hide_index=True,use_container_width=True)
    a=st.radio('Mayor toxicidad aguda:', ['A','B','C','No puede compararse'],index=None,key='q9a')
    b=st.radio('¿Una dosis inferior a la DL₅₀ puede considerarse automáticamente segura?', ['Sí','No'],index=None,key='q9b')
    if st.button('Comprobar',key='b9'): submit(9,a=='A' and b=='No','A tiene la menor DL₅₀ y, por tanto, mayor toxicidad aguda en esta comparación. Estar por debajo de la DL₅₀ **no** equivale a ausencia de toxicidad.','Recuerda: una DL₅₀ menor implica que se necesita menos dosis para alcanzar 50 % de mortalidad.')
    feedback(9); takehome('La DL₅₀ es una medida experimental de letalidad aguda; no constituye un límite individual de seguridad.'); nav()
elif L==10:
    mission('Identifica la dosis experimental más alta sin efecto adverso observado (NOAEL) y la dosis más baja en la que aparece un efecto adverso (LOAEL).')
    concept(['NOAEL','LOAEL'])
    df=pd.DataFrame({'Dosis (mg/kg)':[0,1,5,10,25,50],'Hallazgo':['Sin efecto adverso observado','Sin efecto adverso observado','Sin efecto adverso observado','Elevación adversa de ALT','Lesión hepática','Necrosis hepática']}); st.dataframe(df,hide_index=True,use_container_width=True)
    c1,c2=st.columns(2); n=c1.selectbox('NOAEL',[0,1,5,10,25,50],index=None,key='q10a'); l=c2.selectbox('LOAEL',[0,1,5,10,25,50],index=None,key='q10b')
    if st.button('Comprobar',key='b10'): submit(10,n==5 and l==10,'**NOAEL = 5 mg/kg** y **LOAEL = 10 mg/kg**.','Busca primero la última fila sin efecto adverso y después la primera fila con efecto adverso.')
    feedback(10); takehome('NOAEL y LOAEL dependen de las dosis ensayadas y del diseño del estudio; no son fronteras biológicas exactas.'); nav()
elif L==11:
    mission('Todos ingieren 40 mg del mismo compuesto. Considerando únicamente dosis por kg y F, ¿qué animal presenta la mayor dosis sistémicamente disponible?')
    concept(['Dosis (D)','Biodisponibilidad (F)'])
    df=pd.DataFrame({'Animal':['A','B','C','D'],'Peso (kg)':[10,5,10,20],'Cantidad (mg)':[40]*4,'F':['70 %','70 %','90 %','30 %'],'Condición':['Sano','Sano','Alteración hepática','Sano']}); st.dataframe(df,hide_index=True,use_container_width=True)
    a=st.radio('Seleccione:', ['A','B','C','D'],index=None,key='q11')
    if st.button('Comprobar',key='b11'): submit(11,a=='B','B: 40/5 = 8 mg/kg; 8 × 0,70 = **5,6 mg/kg** sistémicamente disponibles.','Calcula primero mg/kg y después multiplica por F.')
    feedback(11); takehome('La mayor dosis sistémica estimada no determina por sí sola la gravedad: distribución, metabolismo, eliminación y susceptibilidad también importan.'); nav()
elif L==12:
    mission('Un compuesto tiene DL₅₀ oral de 25 mg/kg. Un perro de 10 kg ingiere 100 mg; F = 60 % y presenta disminución del clearance. Selecciona la interpretación más sólida.')
    concept(['Dosis (D)','Biodisponibilidad (F)','DL₅₀','Clearance (CL)','AUC'])
    opts=['La dosis es 10 mg/kg; al estar por debajo de la DL₅₀ puede considerarse segura.','La dosis es 10 mg/kg y la fracción sistémicamente disponible equivale a 6 mg/kg; aun así puede existir toxicidad y el clearance reducido puede aumentar/prolongar la exposición interna.','F = 60 % significa que 60 % de los animales presentará signos.','El clearance no importa porque la dosis administrada ya está definida.']
    a=st.radio('Interpretación:',opts,index=None,key='q12')
    if st.button('Finalizar misión',key='b12'): submit(12,a==opts[1],'La evaluación integra dosis externa, F y eliminación. La DL₅₀ no define un umbral individual de seguridad y un clearance reducido puede incrementar la exposición.','Calcula primero 100/10 y luego aplica F. Después piensa qué ocurre si el compuesto se elimina más lentamente.')
    feedback(12); takehome('La toxicidad observada emerge de la interacción entre exposición, toxicocinética, propiedades del agente y susceptibilidad del organismo.')
    if st.session_state.solved.get(12):
        st.divider(); st.subheader('🏁 Perfil de desempeño')
        groups={'Exposición y dosis':[1,2,3],'Toxicocinética':[4,5,6,7],'Dosis–respuesta y toxicidad':[8,9,10],'Integración del riesgo':[11,12]}
        cols=st.columns(4); rows=[]
        for col,(name,levels) in zip(cols,groups.items()):
            maxp=sum(POINTS[x] for x in levels); earned=0
            for x in levels:
                if st.session_state.solved.get(x):
                    att=st.session_state.attempts.get(x,1); earned+=round(POINTS[x]*(1 if att==1 else .7 if att==2 else .4))
            pct=round(100*earned/maxp); col.metric(name,f'{pct}%'); rows.append((name,pct))
        st.metric('Puntuación global',f'{st.session_state.score}/100')
        weak=[n for n,p in rows if p<75]
        if weak: st.info('**Conceptos para reforzar:** '+', '.join(weak)+'.')
        else: st.success('Desempeño sólido en los cuatro dominios evaluados.')
        st.button('Intentar nuevamente',on_click=reset,type='primary')

st.divider(); st.caption('TOX-LAB 2.0 · Actividad educativa. Los escenarios son pedagógicos y no sustituyen evaluación clínica, experimental o regulatoria real.')
