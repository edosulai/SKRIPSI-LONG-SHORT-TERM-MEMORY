import colorLib from '@kurkle/color'
import 'chartjs-adapter-luxon'

import { createApp, nextTick } from 'vue/dist/vue.esm-browser'
import VueClickAway from "vue3-click-away"
import {
  Chart,
  ArcElement,
  LineElement,
  BarElement,
  PointElement,
  BarController,
  BubbleController,
  DoughnutController,
  LineController,
  PieController,
  PolarAreaController,
  RadarController,
  ScatterController,
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  RadialLinearScale,
  TimeScale,
  TimeSeriesScale,
  Decimation,
  Filler,
  Legend,
  Title,
  Tooltip,
  SubTitle
} from 'chart.js'

Chart.register(
  ArcElement,
  LineElement,
  BarElement,
  PointElement,
  BarController,
  BubbleController,
  DoughnutController,
  LineController,
  PieController,
  PolarAreaController,
  RadarController,
  ScatterController,
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  RadialLinearScale,
  TimeScale,
  TimeSeriesScale,
  Decimation,
  Filler,
  Legend,
  Title,
  Tooltip,
  SubTitle
)

const CHART_COLORS = {
  red: 'rgb(255, 99, 132)',
  orange: 'rgb(255, 159, 64)',
  yellow: 'rgb(255, 205, 86)',
  green: 'rgb(75, 192, 192)',
  blue: 'rgb(54, 162, 235)',
  purple: 'rgb(153, 102, 255)',
  grey: 'rgb(201, 203, 207)'
}

const LOADING = `
  <div class="flex w-20 justify-between mx-auto">
    <span class="flex h-3 w-3 relative">
      <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
      <span class="relative inline-flex rounded-full h-3 w-3 bg-indigo-500"></span>
    </span>
    <span class="flex h-3 w-3 relative">
      <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
      <span class="relative inline-flex rounded-full h-3 w-3 bg-indigo-500"></span>
    </span>
    <span class="flex h-3 w-3 relative">
      <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
      <span class="relative inline-flex rounded-full h-3 w-3 bg-indigo-500"></span>
    </span>
  </div>
`

const transparentize = function (value, opacity) {
  let alpha = opacity === undefined ? 0.5 : 1 - opacity
  return colorLib(value).alpha(alpha).rgbString()
}

const SwitchTheme = createApp({
  data() {
    return {
      isDark: localStorage.getItem('theme') === 'dark' ? true : false
    }
  },
  methods: {
    switcher(event = null) {
      localStorage.theme = typeof event == 'string' ? event : event.target.checked ? 'dark' : 'light'
      if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        this.isDark = true
        document.documentElement.classList.add('dark')
      } else {
        this.isDark = false
        document.documentElement.classList.remove('dark')
      }
    }
  },
  mounted() {
    return this.switcher(localStorage.getItem('theme'))
  }
})
if (document.querySelector('#switch-theme')) SwitchTheme.mount('#switch-theme')

const DropdownTrigger = createApp({
  data() {
    return {
      open: false
    }
  },
  methods: {
    onClickAway() {
      if (this.open) {
        this.open = false
      }
    }
  }
}).use(VueClickAway)
if (document.querySelector('.dropdown-trigger')) DropdownTrigger.mount('.dropdown-trigger')

const Klimatologi = createApp({
  delimiters: ['[[', ']]'],
  data() {
    return {
      klimatologi: {},
      modal_open: false,
      id_to_delete: null,
      prevent_close: false,
    }
  },
  methods: {
    onClickAway() {
      if (this.modal_open && !this.prevent_close) {
        this.modal_open = false
        document.documentElement.style.overflow = 'auto'
      }
      this.prevent_close = false
    },
    modalVisible(event, id, prevent_close) {
      this.modal_open = !this.modal_open
      if (this.modal_open) {
        document.documentElement.style.overflow = 'hidden'
      } else {
        document.documentElement.style.overflow = 'auto'
      }
      this.id_to_delete = id
      this.prevent_close = prevent_close
    },
    redirectToEdit(event, id) {
      window.location.replace(`/klimatologi/${id}/`)
    },
    deleteRow(id) {
      fetch(`/api/klimatologi/${id}/`, {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
      }).then(response => {
        this.modal_open = false
        document.documentElement.style.overflow = 'auto'
        this.klimatologi.ajax.reload()
      }).catch((jqXHR, textStatus, errorThrown) => console.log(errorThrown))
    }
  },
  created() {
    if (!window.redirectToEdit) window.redirectToEdit = this.redirectToEdit
    if (!window.modalVisible) window.modalVisible = this.modalVisible
  },
  mounted() {
    this.klimatologi = $('#klimatologi_table').DataTable({
      processing: true,
      serverSide: true,
      language: {
        processing: LOADING
      },
      ajax: {
        url: "/api/klimatologi/",
        type: "GET",
      },
      columnDefs: [{
        targets: 12,
        orderable: false,
        data: "id",
        render: function (id, type, row, meta) {
          return (`<span class="flex">
                      <button onclick="redirectToEdit(event, ${id})" class="edit-klimatologi flex items-center px-2 py-1 mx-1 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-500 focus:outline-none focus:bg-blue-500">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                              <path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" />
                              <path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" />
                          </svg>
                      </button>
                      <button onclick="modalVisible(event, ${id}, true)" class="flex items-center px-2 py-1 mx-1 bg-red-600 text-white text-sm font-medium rounded-md hover:bg-red-500 focus:outline-none focus:bg-red-500">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                              <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                            </svg>
                      </button>
                  </span>`)
        }
      }],
      columns: [{
        data: "id"
      }, {
        data: "tanggal"
      }, {
        data: "tn"
      }, {
        data: "tx"
      }, {
        data: "tavg"
      }, {
        data: "rh_avg"
      }, {
        data: "rr"
      }, {
        data: "ss"
      }, {
        data: "ff_x"
      }, {
        data: "ddd_x"
      }, {
        data: "ff_avg"
      }, {
        data: "ddd_car"
      }]
    })
  }
}).use(VueClickAway)
if (document.querySelector('#klimatologi')) Klimatologi.mount('#klimatologi')

const PredictionResult = createApp({
  delimiters: ['[[', ']]'],
  data() {
    return {
      connection: new WebSocket('ws://' + window.location.host + '/ws/proyeksi/'),
      terminal: "...\n",
      tablehistori: $('#histori').DataTable({
        processing: true,
        language: {
          zeroRecords: LOADING
        },
        columns: [{
          data: "tanggal"
        }, {
          data: "rr"
        }],
        searching: false,
      }),
      tablepelatihan: $('#pelatihan').DataTable({
        processing: true,
        language: {
          zeroRecords: LOADING
        },
        columns: [{
          data: "tanggal"
        }, {
          data: "rr"
        }],
        searching: false,
      }),
      tableproyeksi: $('#proyeksi').DataTable({
        processing: true,
        language: {
          zeroRecords: LOADING
        },
        columns: [{
          data: "tanggal"
        }, {
          data: "rr"
        }],
        searching: false,
      })
    }
  },
  created() {
    this.chart = new Chart(document.getElementById('predict-chart'), {
      type: 'line',
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Prediksi dan Histori Curah Hujan'
          },
        },
        interaction: {
          intersect: false,
        },
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: 'Timeline'
            }
          },
          y: {
            display: true,
            title: {
              display: true,
              text: 'Tingkat Curah Hujan'
            },
          }
        },
      },
    })
  },
  mounted() {

    this.learning_rate = document.getElementById('learning_rate').innerHTML
    this.dropout = document.getElementById('dropout').innerHTML
    this.sequence = document.getElementById('sequence').innerHTML
    this.max_epoch = document.getElementById('max_epoch').innerHTML
    this.batch_size = document.getElementById('batch_size').innerHTML
    this.hidden_units = document.getElementById('hidden_units').innerHTML
    this.much_predict = document.getElementById('much_predict').getAttribute('value')
    this.nan_handling = document.getElementById('nan_handling').getAttribute('value')

    this.waitForConnection = (callback, interval) => {
      if (this.connection.readyState === 1) {
        callback()
      } else {
        setTimeout(() => {
          this.waitForConnection(callback, interval)
        }, interval)
      }
    }

    this.sendMessage = (message, callback) => {
      this.waitForConnection(() => {
        this.connection.send(message)
        if (typeof callback !== 'undefined') {
          callback()
        }
      }, 1000)
    }

    this.connection.onmessage = (event) => {
      let data = JSON.parse(event.data)
      if (data.message) {
        let terminalElem = document.querySelector("pre")
        let newstring = `${this.terminal}${data.message}`
        let matchstring = newstring.match("\n\.*\r")
        terminalElem.scrollTop = terminalElem.scrollHeight
        if (matchstring != null) {
          this.terminal = newstring.replace(matchstring[0], '\n')
          terminalElem.scrollTop = terminalElem.scrollHeight
        } else {
          this.terminal = newstring
          terminalElem.scrollTop = terminalElem.scrollHeight
        }
      } else if (data.results) {
        let future = data.results.future
        let train = data.results.train
        let histori = data.results.histori

        future[0] = train[train.length - 1]

        this.chart.data = {
          labels: train.concat(future.slice(1, future.length)).map(x => x.tanggal),
          datasets: [
            {
              label: 'Histori',
              data: histori.map(x => x.rr),
              borderColor: CHART_COLORS.blue,
              backgroundColor: transparentize(CHART_COLORS.blue, 0.5),
              fill: false,
              cubicInterpolationMode: 'monotone',
              tension: 0.4
            },
            {
              label: 'Pelatihan',
              data: train.map(x => x.rr),
              borderColor: CHART_COLORS.orange,
              backgroundColor: transparentize(CHART_COLORS.orange, 0.5),
              fill: false,
              cubicInterpolationMode: 'monotone',
              tension: 0.4
            },
            {
              label: 'Prediksi',
              data: train.map(() => null).slice(0, train.length - 1).concat(future.map(x => x.rr)),
              borderColor: CHART_COLORS.red,
              backgroundColor: transparentize(CHART_COLORS.red, 0.5),
              fill: false,
              cubicInterpolationMode: 'monotone',
              tension: 0.4
            }
          ]
        }

        this.chart.update()

        this.tablehistori.rows.add(histori.map(x => {
          return {
            tanggal: x.tanggal,
            rr: x.rr.toFixed(2)
          }
        })).draw()

        this.tablepelatihan.rows.add(train.map(x => {
          return {
            tanggal: x.tanggal,
            rr: x.rr.toFixed(2)
          }
        })).draw()

        this.tableproyeksi.rows.add(future.filter((value, index, arr) => index > 0).map(x => {
          return {
            tanggal: x.tanggal,
            rr: x.rr.toFixed(2)
          }
        })).draw()
      }
    }

    this.sendMessage(JSON.stringify({
      learning_rate: this.learning_rate,
      dropout: this.dropout,
      sequence: this.sequence,
      max_epoch: this.max_epoch,
      batch_size: this.batch_size,
      hidden_units: this.hidden_units,
      much_predict: this.much_predict,
      nan_handling: this.nan_handling
    }))

  }
})
if (document.querySelector('#prediction-result')) PredictionResult.mount('#prediction-result')