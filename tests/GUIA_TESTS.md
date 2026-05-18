# 🧪 Guía de Tests — Cómo usarlos y qué hacen

## Cómo ejecutarlos

### Ejecutar TODOS los tests de golpe
```bash
python -m unittest discover -s tests -v
```
> Esto busca todos los archivos `test_*.py` dentro de la carpeta `tests/` y los ejecuta. La `-v` es de "verbose", para que te muestre cada test con su nombre.

### Ejecutar solo UN archivo de tests
```bash
# Solo los tests de Juego
python -m unittest tests.test_juego -v

# Solo los tests de Pared y Puerta
python -m unittest tests.test_elemento_mapa -v

# Solo los del Builder
python -m unittest tests.test_builder -v
```

### Ejecutar UN test concreto
```bash
# Solo el test de que la puerta abierta deja pasar
python -m unittest tests.test_elemento_mapa.TestPuerta.test_puerta_abierta_pasa_lado1_a_lado2 -v
```

### Interpretar la salida
```
test_pared_no_cambia_posicion ... ok       ← ✅ pasó
test_puerta_cerrada_no_deja_pasar ... FAIL ← ❌ algo falló
test_algo_raro ... ERROR                   ← 💥 el test petó (excepción)

----------------------------------------------------------------------
Ran 148 tests in 0.077s
OK                                          ← todo bien
```

---

## Estructura de un test — Explicación

Cada test sigue siempre el mismo patrón **AAA** (Arrange, Act, Assert):

```python
def test_puerta_abierta_pasa_lado1_a_lado2(self):
    # 1. ARRANGE (preparar) — Creas los objetos necesarios
    self.pj.posicion = self.hab1
    self.puerta.abrir()

    # 2. ACT (actuar) — Ejecutas la acción que quieres probar
    self.puerta.entrar(self.pj)

    # 3. ASSERT (comprobar) — Verificas que pasó lo esperado
    self.assertEqual(self.pj.posicion, self.hab2)
```

### Los asserts más comunes que usamos

| Assert | Qué comprueba | Ejemplo |
|--------|--------------|---------|
| `assertEqual(a, b)` | Que `a == b` | `assertEqual(pj.vidas, 3)` |
| `assertTrue(x)` | Que `x` es `True` | `assertTrue(puerta.abierta)` |
| `assertFalse(x)` | Que `x` es `False` | `assertFalse(pared.es_puerta())` |
| `assertIsNone(x)` | Que `x` es `None` | `assertIsNone(juego.laberinto)` |
| `assertIsNotNone(x)` | Que `x` NO es `None` | `assertIsNotNone(hab.forma)` |
| `assertIn(a, b)` | Que `a` está dentro de `b` | `assertIn(pared, cont.hijos)` |
| `assertIsInstance(a, B)` | Que `a` es de tipo `B` | `assertIsInstance(hab, Contenedor)` |
| `assertIs(a, b)` | Que `a` y `b` son EL MISMO objeto | `assertIs(Norte.default(), Norte.default())` |
| `assertRaises(Error)` | Que lanza esa excepción | `assertRaises(ArchivoConfigError)` |

### `setUp` — Preparación automática

Cuando ves un método `setUp`, ese código se ejecuta **ANTES de cada test** de esa clase:

```python
class TestPuerta(unittest.TestCase):
    def setUp(self):
        # Esto se ejecuta ANTES de CADA test de TestPuerta
        self.hab1 = Habitacion()
        self.hab2 = Habitacion()
        self.puerta = Puerta()
        self.puerta.lado1 = self.hab1
        self.puerta.lado2 = self.hab2

    def test_puerta_abierta(self):
        # Aquí ya tienes self.hab1, self.hab2 y self.puerta listos
        ...
```

---

## Qué hace cada archivo de tests

---

### 📄 `test_elemento_mapa.py` — Pared y Puerta (17 tests)

**¿Qué prueba?** Los elementos básicos del mapa: paredes que bloquean y puertas que abren/cierran.

| Test | Lo que hace en español |
|------|----------------------|
| `test_pared_no_cambia_posicion` | Crea un personaje en hab1, intenta entrar en una pared → comprueba que sigue en hab1 |
| `test_pared_informa_choque` | Choca con pared → comprueba que `ultimo_evento` dice algo de "pared" |
| `test_pared_es_puerta_false` | Una pared NO es puerta |
| `test_pared_es_bomba_false` | Una pared NO es bomba |
| `test_pared_es_salida_false` | Una pared NO es salida |
| `test_pared_str` | `str(Pared())` devuelve `"Pared"` |
| `test_puerta_cerrada_no_deja_pasar` | Puerta cerrada → el personaje se queda donde está |
| `test_puerta_abierta_pasa_lado1_a_lado2` | Puerta abierta desde hab1 → pasa a hab2 |
| `test_puerta_abierta_pasa_lado2_a_lado1` | Puerta abierta desde hab2 → pasa a hab1 |
| `test_puerta_abrir` | Llama `abrir()` → comprueba que `abierta == True` |
| `test_puerta_cerrar` | Abre y cierra → comprueba que `abierta == False` |
| `test_puerta_cerrada_informa` | Puerta cerrada → el evento dice "cerrada" |
| `test_puerta_es_puerta_true` | Una puerta SÍ es puerta |
| `test_puerta_es_bomba_false` | Una puerta NO es bomba |
| `test_puerta_str` | El string de la puerta contiene los números de sus habitaciones |
| `test_puerta_inicia_cerrada` | Una puerta nueva empieza cerrada |

> [!TIP]
> Estos tests cubren la **lógica fundamental** del juego: si la pared no bloquea o la puerta no funciona, todo el juego falla.

---

### 📄 `test_contenedor.py` — Composite (16 tests)

**¿Qué prueba?** El patrón **Composite**: que los contenedores (Habitación, Laberinto) pueden tener hijos y que entrar en una habitación funciona.

| Test | Lo que hace |
|------|-----------|
| `test_agregar_hijo` | Añade un hijo → está en la lista |
| `test_agregar_varios_hijos` | Añade 2 → la lista tiene 2 |
| `test_eliminar_hijo` | Elimina → ya no está |
| `test_eliminar_hijo_inexistente` | Eliminar algo que no existe no peta |
| `test_hijos_inicia_vacio` | Lista vacía al crear |
| `test_entrar_cambia_posicion` | Entrar en hab → `pj.posicion == hab` |
| `test_entrar_actualiza_evento` | Entrar actualiza `ultimo_evento` |
| `test_str_habitacion` | `str(hab)` → `"Hab-3"` |
| `test_habitacion_es_contenedor` | Habitacion hereda de Contenedor |
| `test_habitacion_puede_tener_hijos` | Una hab puede tener hijos (bombas, etc.) |
| `test_agregar_y_obtener_habitacion` | Laberinto: agregar hab y obtenerla por número |
| `test_obtener_habitacion_inexistente` | Pedir hab que no existe → `None` |
| `test_agregar_multiples_habitaciones` | Varias habs, obtener cada una |
| `test_laberinto_entrar_va_a_hab1` | Entrar en laberinto te pone en hab 1 |
| `test_laberinto_es_contenedor` | Laberinto hereda de Contenedor |

---

### 📄 `test_forma.py` — Bridge (9 tests)

**¿Qué prueba?** El patrón **Bridge**: que la forma (Cuadrado) desacopla la geometría del contenedor.

| Test | Lo que hace |
|------|-----------|
| `test_orientaciones_inicia_vacia` | Forma nueva → sin orientaciones |
| `test_agregar_orientacion` | Añadir Norte → está en la lista |
| `test_eliminar_orientacion` | Eliminar → ya no está |
| `test_obtener_orientacion_aleatoria_vacia` | Sin orientaciones → `None` |
| `test_obtener_orientacion_aleatoria` | Con 1 orientación → la devuelve |
| `test_poner_en_elemento` | Poner pared en norte del cuadrado → `cuad.norte == pared` |
| `test_cuadrado_atributos_none_por_defecto` | Cuadrado nuevo: norte/sur/este/oeste = `None` |
| `test_cuadrado_hereda_de_forma` | Cuadrado es una Forma |
| `test_cuadrado_poner_en_4_lados` | Poner pared en los 4 lados funciona |

---

### 📄 `test_orientacion.py` — Singleton (12 tests)

**¿Qué prueba?** El patrón **Singleton**: que cada orientación tiene UNA sola instancia.

| Test | Lo que hace |
|------|-----------|
| `test_norte_singleton` | `Norte.default()` llamado 2 veces → **mismo objeto** (no crea otro) |
| `test_sur/este/oeste_singleton` | Lo mismo para cada orientación |
| `test_norte_no_es_sur` | Norte y Sur son objetos diferentes |
| `test_este_no_es_oeste` | Este y Oeste son objetos diferentes |
| `test_norte/sur/este/oeste_poner_pared` | Cada orientación pone la pared en su lado correcto |
| `test_norte_caminar_pared` | Caminar al norte hacia una pared → no te mueves |

> [!IMPORTANT]
> El test del Singleton (`assertIs`) comprueba que es **exactamente el mismo objeto en memoria**, no solo que son iguales. Eso es lo que hace especial al Singleton.

---

### 📄 `test_modo.py` — State (14 tests)

**¿Qué prueba?** El patrón **State**: que el comportamiento del bicho cambia según su modo.

| Test | Lo que hace |
|------|-----------|
| `test_es_agresivo` | `Agresivo().es_agresivo()` → `True` |
| `test_no_es_perezoso` | `Agresivo().es_perezoso()` → `False` |
| `test_str` (Agresivo) | `str(Agresivo())` → `"Agresivo"` |
| `test_es_perezoso` | `Perezoso().es_perezoso()` → `True` |
| `test_no_es_agresivo` | `Perezoso().es_agresivo()` → `False` |
| `test_str` (Perezoso) | `str(Perezoso())` → `"Perezoso"` |
| `test_modo_base_es_agresivo_false` | Modo base → ni agresivo ni perezoso |
| `test_bicho_con_agresivo_es_agresivo` | Bicho con modo Agresivo → **delega** al modo |
| `test_bicho_con_perezoso_es_perezoso` | Bicho con modo Perezoso → delega |
| `test_bicho_sin_modo_no_es_agresivo` | Sin modo → `False` |
| `test_bicho_str_con_modo` | String del bicho incluye el nombre del modo |
| `test_bicho_str_sin_modo` | Sin modo → dice "SinModo" |

---

### 📄 `test_decorator.py` — Decorator (10 tests)

**¿Qué prueba?** El patrón **Decorator**: que la Bomba "envuelve" otro elemento añadiendo comportamiento.

| Test | Lo que hace |
|------|-----------|
| `test_decorator_sin_elemento` | Decorator nuevo tiene `em = None` |
| `test_decorator_delega_entrar` | Si envuelve una habitación, delega `entrar` a ella |
| `test_decorator_sin_em_no_falla` | Sin elemento envuelto, no peta |
| `test_bomba_es_bomba` | `Bomba().es_bomba()` → `True` |
| `test_bomba_no_es_puerta` | Una bomba no es puerta |
| `test_bomba_inicia_desactivada` | Bomba nueva → `activa = False` |
| `test_bomba_activar` | `activar()` → `activa = True` |
| `test_bomba_desactivar` | `desactivar()` → `activa = False` |
| `test_bomba_activa_no_lanza_error` | Entrar con bomba activa no peta |
| `test_bomba_hereda_de_decorator` | Bomba es un Decorator |

---

### 📄 `test_ente.py` — Combate (14 tests)

**¿Qué prueba?** La mecánica de vida y combate entre personaje y bichos.

| Test | Lo que hace |
|------|-----------|
| `test_vidas_iniciales` | Personaje empieza con 3 vidas |
| `test_poder_inicial` | Personaje empieza con poder 1 |
| `test_posicion_inicial_none` | Empieza sin posición |
| `test_nombre_inicial_vacio` | Empieza sin nombre |
| `test_clase_inicial_alumno` | Empieza como "alumno" |
| `test_dificultad_inicial_normal` | Empieza en "normal" |
| `test_es_atacado_pierde_vidas` | Atacante con poder 3 → víctima pierde 3 vidas |
| `test_es_atacado_varias_veces` | 2 ataques de poder 2 → pierde 4 vidas |
| `test_esta_vivo_true/false` | Vidas > 0 = vivo, vidas ≤ 0 = muerto |
| `test_muere_al_llegar_a_0_vidas` | Al llegar a 0 → `juego.finalizado = True`, `resultado = "derrota"` |
| `test_bicho_vidas_iniciales` | Bicho empieza con 50 vidas |
| `test_bicho_muere` | Matar bicho → 0 vidas, ya no está vivo |

---

### 📄 `test_juego.py` — Factory Method (22 tests)

**¿Qué prueba?** La clase `Juego`: creación de laberintos, personaje, victoria/derrota, gestión de bichos.

| Test | Lo que hace |
|------|-----------|
| `test_juego_sin_laberinto/personaje/bichos` | Juego nuevo está vacío |
| `test_fabricar_lab2_hab` | Crea laberinto con 2 habs |
| `test_fabricar_lab2_hab_fm` | Crea laberinto con FM (formas y orientaciones) |
| `test_fabricar_lab4_hab_fm` | Crea laberinto con 4 habs |
| `test_agregar_personaje` | Crea personaje con nombre |
| `test_personaje_en_hab1` | El personaje aparece en hab 1 |
| `test_gana_personaje` | Victoria: `finalizado=True`, `resultado="victoria"` |
| `test_muere_personaje` | Derrota: `finalizado=True`, `resultado="derrota"` |
| `test_agregar/eliminar_bicho` | Gestión de la lista de bichos |
| `test_hay_bichos_en_habitacion` | Detecta bichos en una hab |
| `test_buscar_personaje` | Encuentra al personaje si está en la misma hab que el bicho |
| `test_abrir/cerrar_puertas` | Abre/cierra TODAS las puertas del laberinto |

---

### 📄 `test_builder.py` — Builder (20 tests)

**¿Qué prueba?** El patrón **Builder**: construcción paso a paso.

| Test | Lo que hace |
|------|-----------|
| `test_fabricar_laberinto` | Crea un `Laberinto` vacío |
| `test_fabricar_habitacion` | Crea hab con num, forma cuadrada y 4 paredes |
| `test_fabricar_habitacion_salida` | Crea hab de salida (es_salida = True) |
| `test_fabricar_puerta` | Crea puerta entre 2 habs en las orientaciones correctas |
| `test_puerta_conecta_habitaciones` | La puerta tiene lado1 y lado2 bien asignados |
| `test_fabricar_juego` | Crea Juego asociado al laberinto |
| `test_fabricar_bicho_agresivo/perezoso` | Crea bichos con el modo correcto |
| `test_fabricar_bomba_en_habitacion` | Pone bomba activa como hija de la hab |
| `test_fabricar_niebla` | Pone niebla activa |
| `test_bomba/niebla_en_hab_inexistente` | Si la hab no existe → `None` (no peta) |

---

### 📄 `test_director.py` — Director del Builder (14 tests)

**¿Qué prueba?** El Director que lee el JSON y construye todo el laberinto.

| Test | Lo que hace |
|------|-----------|
| `test_leer_archivo_json` | Lee `laberinto.json` y parsea los datos |
| `test_archivo_no_encontrado` | Archivo que no existe → lanza `ArchivoConfigError` |
| `test_json_invalido` | JSON malformado → lanza `ArchivoConfigError` |
| `test_ini_builder_poligono4` | Forma "poligono4" → crea `LaberintoBuilder` |
| `test_forma_desconocida` | Forma inválida → lanza error |
| `test_procesar_completo` | `procesar()` crea juego con laberinto completo |
| `test_procesar_crea_habitaciones` | Tras procesar hay habs 1 y 2 |
| `test_procesar_crea_bichos` | Tras procesar hay 2 bichos |
| `test_procesar_hab_salida` | Hab 5 es de salida |
| `test_procesar_timer_global` | Timer global = 300 |
| `test_procesar_json_minimo` | Crea JSON temporal mínimo y lo procesa |

---

## Resumen rápido de comandos

```bash
# Ejecutar TODO
python -m unittest discover -s tests -v

# Ejecutar un archivo
python -m unittest tests.test_modo -v

# Ejecutar un test concreto
python -m unittest tests.test_modo.TestAgresivo.test_es_agresivo -v
```

> [!NOTE]
> Siempre ejecuta desde la raíz del proyecto (la carpeta `Laberinto26-Phyton`), no desde dentro de `tests/`.
