from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

# server = app.server
app.layout = html.Div([
    dcc.Location(id='url'),
    html.Div(id='layout-div'),
    html.Div(id='content')
])

@app.callback(Output('content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    print(pathname)

    if pathname == "/":
        return welcome.layout
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    else:
        return '404'

# @callback(Output('output', 'children'), Input('input', 'value'), prevent_initial_call=True)
# def update_output(value):
#     print('>>> update_output')
#     return value

# @callback(Output('layout-div', 'children'), Input('input', 'value'), prevent_initial_call=True)
# def update_layout_div(value):
#     print('>>> update_layout_div')
#     return value

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8000)