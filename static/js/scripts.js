// This file contains the JavaScript code

function showSection(section) 
{
    const importSections = document.getElementsByName('importsection');
    importSections.forEach(element => {
        element.classList.add('hidden');
    });
    var sectionElement = document.getElementById(section + '-import');
    if (sectionElement.classList.contains('hidden')) {
        sectionElement.classList.remove('hidden');  // Muestra la sección.
    } else {
        sectionElement.classList.add('hidden');  // Oculta la sección.
    }
}

function showConfig(section, correctionId) 
{
    const importSections = document.getElementsByName('config-section');
    importSections.forEach(element => {
        element.classList.add('hidden');
    });
    var sectionElement = document.getElementById(section + '-import-' + correctionId);
    if (sectionElement.classList.contains('hidden')) {
        sectionElement.classList.remove('hidden');
    } else {
        sectionElement.classList.add('hidden');
    }
}
function openDeleteModal(id, element) {
    const form = document.getElementById('deleteForm');
    // Detecta el prefijo del idioma actual en la URL
    const langPrefix = window.location.pathname.split('/')[1];
    form.action = `/${langPrefix}/${element}/delete/${id}/`;
    const modal = document.getElementById('deleteModal');
    const modalInstance = new window.Modal(modal);
    modalInstance.show();
  }
