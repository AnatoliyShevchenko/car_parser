GET_AREAS = """
const regions = [];

window.document.querySelectorAll('li.filter-region__item').forEach(li => {
    const btn = li.querySelector('button');
    const alias = btn.getAttribute('data-alias');
    const label = li.innerText;

    if (label) {
        regions.push({ alias, label });
    }
});
regions;
"""