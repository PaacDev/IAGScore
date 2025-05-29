# Guía de Solución de Errores (Troubleshooting)

Este documento recoge errores comunes y sus soluciones al trabajar con este proyecto.

---

## Error al usar `docker compose` con unidad externa

**Causa:**

Este error ocurre porque Docker Desktop no tiene permisos para acceder a directorios en ciertas unidades del sistema de archivos.

**Solución:**

1. Abre **Docker Desktop**.
2. Ve a `Settings` → `Resources` → `File Sharing`.
3. Añade la ruta del repositorio que estás intentando montar (por ejemplo, `F:\....`).
4. Haz clic en **Apply & Restart** para aplicar los cambios.

**Notas:**
- Asegúrate de tener permisos administrativos para modificar esta configuración.
- Docker Desktop debe estar ejecutándose con suficientes privilegios para acceder a unidades externas o secundarias.

---

_Si encuentras otro error que no esté documentado aquí, por favor abre un issue o contribuye con una solución._
