from dash import Dash, html, dcc, Input, Output, dash_table, State
import plotly.express as px
from conexion_base import DataBase

import dash_bootstrap_components as dbc

app = Dash(__name__, suppress_callback_exceptions=True)


# Dashboard 2 layout
def dashboard2_layout():
    with DataBase() as db:
    # Obtener y procesar los datos
        df_combinado = db.obtener_datos_descuento2()
        df_combinado2 = db.obtenerPreciosDesc()
        df_combinado3 = db.top5Desc()
        df_combinado5 = db.top10Asc()



        # Crear la lista de opciones para el dropdown
        opciones_porcentajes = df_combinado['rango_descuento'].unique()

        # Crear la figura de Plotly Express con el primer porcentaje
        porcentaje_inicial = opciones_porcentajes[0]
        fig_descuento = px.bar(df_combinado, x='Envio', y='cantidad_productos',
                               title=f'Distribución de Descuentos para {porcentaje_inicial}',
                               labels={'Envio': 'Tipo de Envío', 'cantidad_productos': 'Cantidad de Productos'},
                               color='Envio',
                               color_discrete_map={tipo: px.colors.qualitative.Set1[i] for i, tipo in enumerate(df_combinado['Envio'].unique())}
                               )

        figPrecioDesc = px.scatter(df_combinado2, x='Descuento', y='Precio', title='Diagrama de Dispersión',
                         labels={'Precio': 'Precio', 'Descuento': 'Descuento'}, hover_data=['Nombre'], color='Descuento',
                                   color_continuous_scale='Virdis')


    # Diseño de la aplicación
        return html.Div([
            html.H2("Dashboard 2", style={"color": "black"}),
            html.P("Contenido del segundo dashboard"),
            # Dropdown para seleccionar el porcentaje de descuento
            html.Label("Seleccionar Porcentaje de Descuento:"),
            dcc.Dropdown(
                id='dropdown-porcentaje',
                options=[{'label': 'ALL', 'value': 'ALL'}] + [{'label': porcentaje, 'value': porcentaje} for porcentaje in opciones_porcentajes],
                value=porcentaje_inicial
            ),
            dcc.Graph(figure=fig_descuento, id='descuento-graph'),

            html.Div([
                html.H2("Top 10 Productos con Mayores Descuentos", style={"color": "black"}),

                html.Div([ html.Table( [html.Tr([html.Th(col) for col in df_combinado3.columns])] +
                        [html.Tr([html.Td(df_combinado3.iloc[i][col]) for col in df_combinado3.columns]) for i in
                         range(len(df_combinado3))]
                    ),
                ], style={'overflowX': 'auto', 'width':'50%', 'float':'left', 'display': 'inline-block'})]),

            html.Div([
                html.H2("Top 10 Productos con Menor Descuentos", style={"color": "black"}),

                html.Div([html.Table([html.Tr([html.Th(col) for col in df_combinado5.columns])] +
                                     [html.Tr([html.Td(df_combinado5.iloc[i][col]) for col in df_combinado5.columns])
                                      for i in
                                      range(len(df_combinado5))]
                                     ),
                          ], style={'overflowX': 'auto', 'width': '50%', 'float': 'center', 'display': 'inline-block'}),
            ]),

                html.Div([
                dcc.Graph(figure=figPrecioDesc , id='tipo-graph-pie'),
            ], style={'width': '100%', 'display': 'inline-block', 'float': 'center'}),
        ])


@app.callback(
    Output('descuento-graph', 'figure'),
    [Input('dropdown-porcentaje', 'value')]
)
def actualizar_grafico(porcentaje_seleccionado):
    with DataBase() as db:
        df_combinado = db.obtener_datos_descuento2()

        # Filtrar el DataFrame según el porcentaje seleccionado
    if porcentaje_seleccionado == 'ALL':
        df_filter = df_combinado
        title_text = 'Distribución de Descuentos para TODOS los Porcentajes'
    else:
        df_filter = df_combinado[df_combinado['rango_descuento'] == porcentaje_seleccionado]
        title_text = f'Distribución de Descuentos para {porcentaje_seleccionado}'

    tipos_disponibles_descuento = df_combinado['Envio'].unique()

    nueva_figura = px.bar(df_filter, x='Envio', y='cantidad_productos',
                          title=title_text,
                          labels={'Envio': 'Tipo de Envío', 'cantidad_productos': 'Cantidad de Productos'},
                          color='Envio',
                          color_discrete_map={tipo: px.colors.qualitative.Set1[i] for i, tipo in
                                              enumerate(tipos_disponibles_descuento)}
                          )

    return nueva_figura



if __name__ == '__main__':
    app.layout = dashboard2_layout
    app.run_server(debug=True)