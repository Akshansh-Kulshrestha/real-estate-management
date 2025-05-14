document.addEventListener('DOMContentLoaded', function () {
    const fieldsets = document.querySelectorAll('.form-row .checkboxselectmultiple ul');

    fieldsets.forEach(ul => {
        const groupItems = ul.querySelectorAll('li');
        if (groupItems.length === 0) return;

        // Extract the model name from the first permission (assumes format "Can add ModelName")
        const firstLabel = groupItems[0].querySelector('label');
        if (!firstLabel) return;

        const labelText = firstLabel.innerText;
        const modelMatch = labelText.match(/Can\s(?:add|change|delete|view)\s(.+)/i);
        if (!modelMatch) return;

        const modelName = modelMatch[1].trim();

        // Create "Select All" checkbox
        const selectAllLabel = document.createElement('label');
        selectAllLabel.style.fontWeight = 'bold';
        selectAllLabel.style.display = 'block';
        selectAllLabel.style.marginBottom = '6px';

        const selectAllCheckbox = document.createElement('input');
        selectAllCheckbox.type = 'checkbox';
        selectAllCheckbox.style.marginRight = '6px';

        selectAllCheckbox.addEventListener('change', () => {
            groupItems.forEach(item => {
                const input = item.querySelector('input[type=checkbox]');
                if (input) input.checked = selectAllCheckbox.checked;
            });
        });

        selectAllLabel.appendChild(selectAllCheckbox);
        selectAllLabel.appendChild(document.createTextNode(`Select all ${modelName}`));

        // Insert above the group
        ul.parentElement.insertBefore(selectAllLabel, ul);
    });
});
