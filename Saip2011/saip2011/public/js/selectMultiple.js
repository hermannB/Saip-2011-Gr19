function selectMultiple()
{	
	var selectItem = document.getElementsByTagName('select');
	
	for(i = 0; i < selectItem.length; i++)
	{
		if(selectItem[i].multiple)
		{
			selectItem[i].style.display = 'none';
			selectItem[i].style.visibility = 'hidden';
			
			// Creamos el elemento UL de la nueva lista y le aplicamos una clase
			var ulSelect = document.createElement("UL");
				ulSelect.className = "selectMultiple";
				
			// Aplicamos al "nuevo select" los estilos de posicion y tamaño que pudiera tener el original
			if(selectItem[i].style.width) ulSelect.style.width = selectItem[i].style.width;
			if(selectItem[i].style.height) ulSelect.style.height = selectItem[i].style.height;
			if(selectItem[i].style.position) ulSelect.style.position = selectItem[i].style.position;
			if(selectItem[i].style.left) ulSelect.style.left = selectItem[i].style.left;
			if(selectItem[i].style.top) ulSelect.style.top = selectItem[i].style.top;
			if(selectItem[i].style.right) ulSelect.style.right = selectItem[i].style.right;
			if(selectItem[i].style.bottom) ulSelect.style.bottom = selectItem[i].style.bottom;
			
			// Buscamos los value del SelectBox
			liEls = selectItem[i].getElementsByTagName("option");
			
			for(e = 0; e < liEls.length; e++)
			{
				// Creamos la lista
				liSelect = document.createElement("LI")
				
				// Comprobamos si el SelectBox original tiene algún option seleccionado
				if(liEls[e].selected == true)
				{
					liSelect.className = "selected";
				}
				
				// Creamos dos variables que nos muestre tanto el estado de selección del elemento como la posición que ocupa
				liSelect.selected	= liEls[e].selected;
				liSelect.selectC	= liEls[e];
				liSelect.e			= e;
				liSelect.i			= i;
				
				// Creamos el texto para la lista
				textLi = document.createTextNode(liEls[e].text);
				
				// Acoplamos ese texto a cada lista
				liSelect.appendChild(textLi);
				
				// Incluimos el evento que nos permite marcar y desmarcar el elemento seleccionado
				liSelect.onclick = function(e,i)
									{
										if(this.className && this.className == "selected")
										{
											// Eliminamos la clase, no sin antes aplicar la regla según el navegador >:-(
											if (navigator.appName == 'Microsoft Internet Explorer')
											{
												this.removeAttribute("className");
											} else {
												this.removeAttribute("class");
											}
											
											// Deseleccionamos el elemento original
											selectItem[this.i].getElementsByTagName("option")[this.e].selected = false;
										} else {
											this.className = "selected";
											// Seleccionamos el elemento original
											selectItem[this.i].getElementsByTagName("option")[this.e].selected = true;
										}
									}
				
				// Y acoplamos ese elemento al UL principal
				ulSelect.appendChild(liSelect);
			}	
			
			// Colocamos el nuevo SelectMultiple en el documento
			document.body.appendChild(ulSelect);
			
			// Y lo posicionamos justo antes del Select Original
			selectItem[i].parentNode.insertBefore(ulSelect,selectItem[i]);
		}
	}
}

// Esta función nos permite añadir una acción al evento onLoad
function addLoadEvent(func) 
{
	var oldonload = window.onload;
	if (typeof window.onload != 'function') 
		{
			window.onload = func;
		} else {
			window.onload = function() 
				{
					oldonload();
					func();
				}
		}
}

// Ejecutamos directamente la función SelectMultiple
addLoadEvent(selectMultiple);