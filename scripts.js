/**
 * BioChavez Forester - Navigation & UX Engine
 * Implementación de Clean URLs y Scroll Suave
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Control del Menú Hamburguesa
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            hamburger.classList.toggle('toggle');
        });

        // Cerrar menú al hacer clic en un enlace (excepto si es un disparador de submenú)
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                hamburger.classList.remove('toggle');
            });
        });
    }

    // 2. Motor de Scroll Suave y URLs Limpias
    const scrollToSection = (targetId, cleanUrl = true) => {
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
            const navHeight = document.querySelector('nav').offsetHeight;
            const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - navHeight;

            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });

            // Limpieza de la URL: elimina el hash de la barra de direcciones
            if (cleanUrl) {
                history.replaceState(null, null, window.location.pathname);
            }
        }
    };

    // Escuchar clics en elementos con data-scroll
    document.querySelectorAll('[data-scroll]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('data-scroll');
            
            // Si estamos en la página principal, hacemos scroll directo
            if (document.getElementById(targetId)) {
                scrollToSection(targetId);
            } else {
                // Si no, redireccionamos a la home con el parámetro
                window.location.href = `/?goto=${targetId}`;
            }
        });
    });

    // 3. Manejo de redirecciones desde subpáginas (Auto-Scroll)
    const urlParams = new URLSearchParams(window.location.search);
    const goto = urlParams.get('goto');
    
    if (goto) {
        // Pequeño delay para asegurar que el DOM y las imágenes se carguen
        setTimeout(() => {
            scrollToSection(goto, true);
            // Limpia el parámetro de la URL después del scroll
            const cleanUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
            window.history.replaceState({path: cleanUrl}, '', cleanUrl);
        }, 500);
    }
});
