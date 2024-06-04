function getQueryParam(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

function setActiveListFromUrl() {
    const activeListId = getQueryParam('active');
    if (activeListId) {
        const activeList = document.getElementById(activeListId);
        if (activeList) {
            activeList.classList.add('active');
            activeList.querySelectorAll('.vertical-line-column, a').forEach(function(element) {
                element.classList.add('active');
            });
        }
    }
}

window.addEventListener('load', setActiveListFromUrl);