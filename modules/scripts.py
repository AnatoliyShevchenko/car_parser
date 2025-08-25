GET_AREAS = """
const regions = [];

window.document.querySelectorAll('li[data-test="filter-region-item"]').forEach(li => {
    const btn = li.querySelector('button');
    const alias = btn?.getAttribute('data-alias');
    const label = li.querySelector('span[data-test="filter-item-label"]')?.textContent.trim();

    if (label) {
        regions.push({ alias, label });
    }
});
"""