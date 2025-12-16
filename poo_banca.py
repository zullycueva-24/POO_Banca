import streamlit as st                      # Importa la librería Streamlit y la nombra 'st' para crear UI web simple en Python.
from datetime import datetime               # Importa 'datetime' para obtener fecha y hora actual y registrar movimientos.

st.title("💵 Transacciones Bancarias")  # Coloca un título visible en la parte superior de la app web.

class Cuenta:                               # Define una clase 'Cuenta' (POO) que modela una cuenta bancaria con saldo.
    def __init__(self, titular, saldo=0):   # Método constructor: se ejecuta al crear una instancia; recibe titular y saldo inicial.
        self.titular, self.saldo = titular, saldo  # Asigna a la instancia (self) el nombre del titular y el saldo actual.
    def depositar(self, m): self.saldo += m        # Método de negocio: suma 'm' al saldo; NO valida negativo (se controla en la UI).
    def retirar(self, m):                          # Método de negocio: intenta retirar 'm' del saldo actual.
        if m <= self.saldo: self.saldo -= m        # Solo descuenta si hay fondos suficientes (evita sobregiros); si no, no hace nada.

c = st.session_state.setdefault("c", Cuenta("Carlos", 100))  # Usa el estado de sesión de Streamlit:
                                                             # - Si no existe la clave 'c', crea una Cuenta("Carlos",100) y la guarda.
                                                             # - Si ya existe, devuelve la cuenta existente (persiste entre reruns).
h = st.session_state.setdefault("h", [])                     # En 'h' guardamos el historial: si no existe, crea una lista vacía.

m = st.number_input("Monto", 0, 1000, 50)                    # Crea un input numérico:
                                                             # - Etiqueta "Monto"
                                                             # - Mínimo 0 (evita negativos), máximo 1000, valor por defecto 50.

if st.button("Depositar"):                                   # Renderiza un botón "Depositar"; devuelve True solo en el clic actual.
    c.depositar(m)                                           # Llama al método de la cuenta para sumar 'm' al saldo.
    h.append(f"{datetime.now():%Y-%m-%d %H:%M:%S} · Depósito · ${m} · Saldo ${c.saldo}")  # Agrega una línea al historial con:
                                                             # - Timestamp 'YYYY-MM-DD HH:MM:SS'
                                                             # - Tipo de operación (Depósito)
                                                             # - Monto depositado
                                                             # - Saldo resultante después del depósito

if st.button("Retirar"):                                     # Renderiza un botón "Retirar"; True únicamente en el clic actual.
    saldo_prev = c.saldo                                     # Guarda el saldo antes de intentar el retiro (para saber si cambió).
    c.retirar(m)                                             # Intenta retirar 'm' usando la regla de negocio (no sobregirar).
    if c.saldo < saldo_prev:                                 # Si el saldo bajó, significa que el retiro fue exitoso.
        h.append(f"{datetime.now():%Y-%m-%d %H:%M:%S} · Retiro   · ${m} · Saldo ${c.saldo}")  # Registra el retiro con:
                                                             # - Timestamp
                                                             # - Tipo de operación (Retiro)
                                                             # - Monto retirado
                                                             # - Saldo resultante
    else:                                                    # Si el saldo NO cambió, no había fondos suficientes para retirar.
        st.warning("Fondos insuficientes.")                  # Muestra un aviso visual (amarillo) al usuario.

st.write(f"👤 {c.titular} — Saldo: ${c.saldo}")              # Muestra en pantalla el titular y el saldo actual usando un f-string.

st.subheader("🧾 Historial")                                  # Subtítulo para la sección de historial.
st.text("\n".join(reversed(h)) if h else "Aún sin movimientos.")  # Muestra el historial como texto:
                                                                  # - Si hay movimientos, los invierte para ver el más reciente arriba.
                                                                  # - Si no hay, muestra "Aún sin movimientos."
