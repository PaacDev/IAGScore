// This file contains the JavaScript code

function showSection(section) 
{
    if (document.getElementById('import-section').classList.contains('hidden')) {
        document.getElementById('import-section').classList.remove('hidden');
    } else {
        document.getElementById('import-section').classList.add('hidden');
    }
}
