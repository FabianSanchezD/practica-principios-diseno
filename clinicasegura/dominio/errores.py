class ErrorDominio(Exception):
    """Falla de negocio. El borde la traduce a una respuesta; una falla
    técnica, en cambio, no hereda de aquí y sube sin disfraz."""


class RecetaInvalida(ErrorDominio):
    """Los datos recibidos no describen una receta emitible."""


class CadenaNoSoportada(ErrorDominio):
    """Se pidió despachar por una cadena que nadie sabe atender."""


class FarmaciaNoDisponible(ErrorDominio):
    """La cadena existe pero no aceptó la receta en este momento."""
