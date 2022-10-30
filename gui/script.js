const file_input = document.getElementById('file')
let file = null

function ArrayBuffer2Array(ab = new ArrayBuffer) {
    return Array.from(new Uint8Array(ab))
}

function createTable(data={fields: [``], rows: [{id: 1, data: {}}]}, onRowSelect = () => {}) {
    let f_data = [], fields = data.fields, columns = {}
    for (let i = 0; i < data.fields.length; i++) {
        const field = data.fields[i];
        let obj = {
            header: field,
            rows: []
        }
        for (const row of data.rows) {
            if (typeof row[field] != `number` && typeof row[field] != `string`) {
                obj.rows.push(JSON.stringify(row[field]))
                continue
            }
            obj.rows.push(row[field])
        }
        f_data.push(obj)
    }
    let domElement = document.createElement(`div`)
    domElement.classList.add(`table`)

    for (const column of f_data) {
        let table_column = document.createElement(`div`),
            header = document.createElement(`div`)
        table_column.classList.add(`table-column`)
        header.classList.add(`header`)
        header.innerHTML = column.header == `id` ? column.header.toUpperCase() : `${column.header[0].toUpperCase()}${column.header.slice(1).toLowerCase()}`
        table_column.append(header)
        columns[column.header] = table_column
        for (let i = 0; i < column.rows.length; i++) {
            const row = column.rows[i]
            let row_elem = document.createElement(`div`)
            row_elem.classList.add(`row`)
            if (column.header == `data`) {
                row_elem.addEventListener(`click`, (e) => {
                    let id = -1
                    if (f_data[0].header === `id`) {
                        id = Number(f_data[0].rows[i])
                    }
                    try {
                        onRowSelect(id, JSON.parse(e.target.textContent))
                    } catch (error) {
                        onRowSelect(id, e.target.textContent)
                    }
                })
            }
            row_elem.innerHTML = (column.header != `login` && column.header != `password`) ? row : `<i>${column.header}</i>`
            table_column.append(row_elem)
        }
        domElement.append(table_column)
    }

    return {
        domElement,
        addLine: (row) => {
            let f_data = []
            for (let i = 0; i < fields.length; i++) {
                const field = fields[i];
                let obj = {
                    header: field,
                    rows: []
                }
                if (typeof row[field] != `number` && typeof row[field] != `string`) {
                    obj.rows.push(JSON.stringify(row[field]))
                } else {
                    obj.rows.push(row[field])
                }
                f_data.push(obj)
            }
            for (const column of f_data) {
                let table_column = columns[column.header]
                for (let i = 0; i < column.rows.length; i++) {
                    const row = column.rows[i]
                    let row_elem = document.createElement(`div`)
                    row_elem.classList.add(`row`)
                    if (column.header == `data`) {
                        row_elem.addEventListener(`click`, () => {
                            let id = -1
                            if (f_data[0].header === `id`) {
                                id = Number(f_data[0].rows[i])
                            }
                            try {
                                onRowSelect(id, JSON.parse(row))
                            } catch (error) {
                                onRowSelect(id, row)
                            }
                        })
                    }
                    row_elem.innerHTML = (column.header != `login` && column.header != `password`) ? row : `<i>${column.header}</i>`
                    table_column.append(row_elem)
                }
            }
        },
        updateLine: (id, data) => {
            for (const column in columns) {
                try {
                    columns[column].querySelectorAll(`.row`)[id - 1].innerHTML = typeof data[column] === `object` ? JSON.stringify(data[column]) : data[column]
                } catch (err) {
                    continue
                }
            }
        },
        removeLine: (id) => {
            for (const column in columns) {
                columns[column].querySelectorAll(`.row`)[id - 1].remove()
            }
        }
    }
}

const names = {
    acc_desc: 'Точность описания',
    // acc_name: 'Точность названия',
    valid_url: 'Валидность ссылки на сайт',
    valid_techs: 'Валидность технологий',
    valid_branch: 'Валидность отраслей',
    site_is_available: 'Доступность сайта',
}

function openMenu (data) {
    const menu = document.getElementById('info-menu')
    const close_btn = document.getElementById('info-close-btn')


}

function load_data(data) {
    console.log(data)
    let item = document.createElement('div')
    let item_name = document.createElement('div')
    item.classList.add('item')
    item_name.classList.add('item-name')

    item_name.innerText = data.row[1]

    item.append(item_name)
    document.querySelector('.items').append(item)
}
function end_processing() {
    document.querySelector('progress-bar').classList.add('success')
    setTimeout(() => {
        document.querySelector('progress-bar').style.display = "none"
    }, 1500)
}
eel.expose(load_data)
eel.expose(end_processing)

file_input.addEventListener('input', (e) => {
    document.querySelector('progress-bar').style.display = ""
    const fr = new FileReader()
    fr.addEventListener(`load`, () => {
        eel.load_file('data.xlsx', ArrayBuffer2Array(fr.result))
        eel.process_data()
    })
    file = file_input.files[0]
    file_input.setAttribute('file-name', file.name)
    fr.readAsArrayBuffer(file)
})

class ProgressBar extends HTMLElement {
    constructor() {
        super();
    }

    get value () {
        if (this.hasAttribute(`value`)) {
            return Number(this.getAttribute(`value`))
        }
        return 0
    }

    set value (v) {
        this.setAttribute(`value`, String(v))
    }

    connectedCallback() {
        setTimeout(() => {
            if (this.hasAttribute(`value`)) {
                this.style.setProperty(`--value`, this.getAttribute(`value`)+'%')
            }
        })
    }

    disconnectedCallback() {}

    static get observedAttributes() {
        return ['value'];
    }

    attributeChangedCallback(name, oldValue, newValue) {
        if (name == `value`) {
            this.style.setProperty(`--value`, `${newValue}%`)
        }
    }

    adoptedCallback() {}
}
customElements.define("progress-bar", ProgressBar);
