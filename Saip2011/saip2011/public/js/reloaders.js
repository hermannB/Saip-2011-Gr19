/* 
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */


   function reloadProducto(selector)
    {
        if (selector.value != "" )
        {
	    var nombre = selector.value;
	     alert ("hola");
	       // obtenemos el listado de poblaciones del xml de respuesta del servicio
	       var items = response.responseXML.getElementsByTagName("list_fase");

	       // prototype getElementById: obtenemos el selector de poblaciones del árbol DOM
	       var imput = $("nombre_fase");
	      
	      imput = nombre;
      }
   }

   function mensaje(){
              alert ("hola")
		
         }


