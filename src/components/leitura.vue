<template>
  <div id="app">
    <v-card class="card" color="#c6c6c6" outlined shaped>
      <div class="card-title"><b>Leitor de distância</b></div>
      <div class="card-sub">Leitura com ESP32 e HC-SR04.</div>
      <div class="card-dist">{{esp}} cm</div>
      <div class="gauge">
        <GChart
          :settings="{ packages: ['Gauge'] }"
          type="Gauge"
          :data="chartDist"
          :options="chartODist"
        />
      </div>
      <div class="btn-led">
        <p id="espaco">LED ON/OFF:</p>
        <v-btn icon @click="clickPub">
          <v-icon v-if="ledOn" color="#008000" large>mdi-power-standby</v-icon>
          <v-icon v-if="ledOff" color="#ff0000" large>mdi-power-standby</v-icon>
        </v-btn>

      </div>
    </v-card>
  </div>
</template>


<script>
export default {
  name: "leitura",

  props: {
    esp: {type: String, default: "00.00 cm"}
  },

  data() {
    return {
      // led power on-off
      ledOn: false,
      ledOff: true,

      // Array will be automatically processed with visualization.arrayToDataTable function
      chartDist: [
        ['Label', 'Value'],
        ['Distância', 0]
      ],
      chartODist: {
        width: 450, height: 150,
        greenFrom: 0, greenTo: 100,
        redFrom: 300, redTo: 400,
        yellowFrom: 100, yellowTo: 300,
        minorTicks: 5, min: 0, max: 400
      },
    }
  },

  mqtt: {
    "laura/#" : function (data, topics) {
      if ('laura/sensor' === topics) {
        let dist = String.fromCharCode.apply(null, data)
        this.chartDist = [
            ['Label', 'Value'],
            ['Distância', Number(dist)]
        ]
        this.esp = dist
      }
    }
  },

  methods: {
    clickPub: function() {
      if (this.ledOff === true) {
        this.$mqtt.publish('laura/led', '1')
        this.ledOff = false
        this.ledOn = true
      } else {
        this.$mqtt.publish('laura/led', '0')
        this.ledOff = true
        this.ledOn = false
      }
    }
  }
}
</script>


<style scoped>
.card {
  width: 400px;
  height: 375px;
  margin: auto;
  text-align: center;
  box-shadow: 2px 2px 8px black;
}

.card-title {
  margin-top: 20px;
  font-size: 1.8em;
}

.card-sub {
  margin-top: 10px;
  font-size: 0.9em;
}

.card-dist {
  margin-top: 25px;
  font-size: 1.5em;
}

.btn-led {
  margin-top: 25px;
}

#espaco {
  margin-bottom: 5px;
}

.gauge {
  width: 152px;
  margin: auto;
}
</style>
