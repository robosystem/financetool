import streamlit as st
from streamlit_echarts import st_echarts

st.title("Strategie di trading")
st.write("Qualsiasi investimento comporta un determinato grado di rischio, inclusa la possibile \
perdita di capitale. Non vi è alcuna garanzia che gli obiettivi di investimento della strategia \
saranno raggiunti. Il presente strumento non intende pertanto costituire una raccomandazione o un \
consiglio di investimento, né costituisce una sollecitazione all’acquisto o alla vendita \
di titoli. Le informazioni elaborate non tengono conto di specifiche circostanze od obiettivi \
di un particolare investitore: le decisioni di investimento dovrebbero essere prese in base agli \
obiettivi e alle circostanze di chi opera e in consultazione con i propri consulenti.")
st.write("## Ingresso")
acquisto  = round(st.number_input("Prezzo d'acquisto", min_value=0.0), 2)
qta = st.number_input("Quantità", min_value=0)
volume = round(acquisto*qta, 2)
st.write("Investimento", volume)
target = st.number_input("Target", min_value=0.0)
if target > 0 and volume > 0:
	st.write("Controvalore obiettivo", round(qta*target, 2))
	increment = ((qta*target)-(qta*acquisto))/volume
	profitto = round((qta*target)-volume,2)
	st.write("Guadagno atteso", f'{increment:.2%}'+" ("+str(profitto)+")")
stop = st.number_input("Stop Loss", min_value=0.0)
if stop > 0 and volume > 0:
	st.write("Controvalore minimo", round(qta*stop, 2))
	decrement = ((qta*stop)-(qta*acquisto))/volume
	perdita = round((qta*stop)-volume,2)
	st.write("Perdita attesa", f'{decrement:.2%}'+" ("+str(perdita)+")")
if target > 0 and stop > 0:
	st.header("Strategia")
	options = {
		#"title": {"text": "Strategia"},
		"toolbox": {"feature": {"saveAsImage": {}}},
		"tooltip": {
			"show": "true",
		    "trigger": "axis",
		    "triggerOn": "click",
		},
		"legend": {"data": ["strumento", "take profit", "stop loss"]},
		"grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
		"xAxis": {
		    "type": "category",
			"boundaryGap": False,
			"data": ["Inizio", "Fine"],
		},
		"yAxis": {"type": "value"},
		"series": [
	        {
	            "name": "strumento",
	            "type": "line",
				"smooth": "true",
	            "stack": "strumento",
	            "data": [acquisto, acquisto],
				"itemStyle": {
					"color": 'blue'
				},
				"lineStyle": {
			        "normal": {
			          "color": 'blue',
			          "width": 4,
					}
				}
	        },
	        {
	            "name": "take profit",
				"label": {
					"show": "true",
					"formatter": f'{increment:.2%}',
				},
	            "type": "line",
				"smooth": "true",
	            "stack": "take profit",
	            "data": [target, target],
				"itemStyle": {
					"color": 'green'
				},
				"lineStyle": {
			        "normal": {
			          "color": 'green',
			          "width": 2,
			          "type": 'dashed'}
				}
	        },
	        {
	            "name": "stop loss",
				"label": {
					"show": "true",
					"formatter": f'{decrement:.2%}',
				},
	            "type": "line",
				"smooth": "true",
	            "stack": "stop loss",
	            "data": [stop, stop],
				"itemStyle": {
					"color": 'red'
				},
			    "lineStyle": {
			        "normal": {
			          "color": 'red',
			          "width": 2,
			          "type": 'dashed'}
				}
	        },
		],
	};
	st_echarts(options=options, height="500px")

cont = st.checkbox("Rimodula la strategia per le attuali condizioni del mercato")
if cont:
	st.write("## Rimodulazione")
	deal = st.number_input("Commissioni (opzionale)", min_value=0.0)
	prezzo = st.number_input("Prezzo attuale mercato", min_value=0.0)
	max = st.number_input("Quantità massima da aggiungere", min_value=1)
	add = st.slider("Simulazione incremento posizione", 1, max, int(max/2), key=1)
	costo = round(add*prezzo+deal, 2)
	if add > 0 and qta > 0:
		new = round((volume+costo)/(add+qta), 2)
		st.write("Nuova posizione", new)
		st.write("Costo incremento", costo)

		if acquisto > 0 and prezzo > 0:
			st.write("Quantità complessiva", qta+add)
			st.write("Nuovo controvalore", round(volume+costo,2))

			riepilogo = {
				#"title": {"text": "Rimodulazione"},
				"toolbox": {"feature": {"saveAsImage": {}}},
				"tooltip": {
					"show": "true",
				    "trigger": "axis",
				    "triggerOn": "click",
				},
				"legend": {"data": ["posizione", "ipotesi", "take profit", "stop loss", "prezzo"]},
				"grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
				"xAxis": {
				    "type": "category",
					"boundaryGap": False,
					"data": ["Inizio", "Ipotesi", "Fine"],
				},
				"yAxis": {"type": "value"},
				"series": [
					{
						"name": "posizione",
						"type": "line",
						"smooth": "true",
						"stack": "posizione",
						"data": [acquisto, acquisto, 'null'],
						"itemStyle": {
							"color": 'blue'
						},
						"lineStyle": {
					        "normal": {
					          "color": 'blue',
					          "width": 4,
					        }
						}
					},
					{
						"name": "prezzo",
						"type": "line",
						"smooth": "true",
						"stack": "prezzo",
						"data": [acquisto, prezzo, prezzo],
						"itemStyle": {
							"color": 'orange'
						},
						"lineStyle": {
					        "normal": {
					          "color": 'orange',
					          "width": 2,
					        }
						}
					},
			        {
			            "name": "ipotesi",
			            "type": "line",
						"smooth": "true",
			            "stack": "ipotesi",
			            "data": ['null', new, new],
						"itemStyle": {
							"color": 'blue',
							"type": 'dashed'
						},
						"lineStyle": {
					        "normal": {
					          "color": 'blue',
					          "width": 2,
					          "type": 'dashed'}
						}
			        },
			        {
			            "name": "take profit",
			            "type": "line",
						"smooth": "true",
			            "stack": "take profit",
			            "data": [target, target, target],
						"itemStyle": {
							"color": 'green'
						},
						"lineStyle": {
					        "normal": {
					          "color": 'green',
					          "width": 2
							}
						}
			        },
			        {
			            "name": "stop loss",
			            "type": "line",
						"smooth": "true",
			            "stack": "stop loss",
			            "data": [stop, stop, stop],
						"itemStyle": {
							"color": 'red'
						},
						"lineStyle": {
					        "normal": {
					          "color": 'red',
					          "width": 2
							}
						}
			        },
				],
			}
			st_echarts(options=riepilogo, height="500px")

			#-195.96 (-21.49%)
			hyp_increment = (target*(qta+add)-(volume+costo))/(volume+costo)
			hyp_profitto = round((target*(qta+add)-(volume+costo)),2)
			hyp_decrement = (stop*(qta+add)-(volume+costo))/(volume+costo)
			hyp_perdita = round((stop*(qta+add)-(volume+costo)),2)
			delta_increment = hyp_increment-increment
			delta_decrement = decrement-hyp_decrement
			col1, col2, col3 = st.columns(3)
			with col1:
				st.write("#### Strategia")
				st.write("Profitto", f'{increment:.2%}'+" ("+str(profitto)+")")
				st.write("Perdita ", f'{decrement:.2%}'+" ("+str(perdita)+")")
			with col2:
				st.write("#### Rimodulazione")
				st.write("Profitto", f'{hyp_increment:.2%}'+" ("+str(hyp_profitto)+")")
				st.write("Perdita ", f'{hyp_decrement:.2%}'+" ("+str(hyp_perdita)+")")
			with col3:
				st.write("#### Δ")
				st.write("Profitto", f'{(delta_increment):.2%}')
				st.write("Perdita ", f'{(delta_decrement):.2%}')
