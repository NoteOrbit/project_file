<template>
  
  <div class="q-pa-md q-gutter-sm row justify-center">
    
    <q-btn @click=onNext style="background: black; color: white" label="Next M" />
    <q-btn @click=onToday outline style="color: green" label="To Day" />
  </div>
  
  <div class="row justify-center">
    
    <div style="display: flex; justify-content: center; align-items: center; flex-wrap: nowrap;">
    </div>
    <div style="display: flex; max-width: 800px; width: 100%;">
      <q-calendar-month ref="calendar" v-model="selectedDate" animated bordered focusable hoverable no-active-date
        :day-min-height="60" :day-height="0" @click-date="onClickDate" @click-day="onClickDay" @change="onChange"
        @moved="onNext">
        <template #day="{ scope: { timestamp } }">
          <template v-for="event in eventsMap[timestamp.date]" :key="event.id">
            <div :class="badgeClasses(event, 'day')"  class="my-event">
              <div class="title q-calendar__ellipsis">
                <q-icon name="model_training" />{{ event.id }}
                <q-tooltip>{{ event.time }}</q-tooltip>
              </div>
            </div>
          </template>
        </template>
      </q-calendar-month>
      
    </div>
  </div>
  <q-dialog v-model="showDialog">
    <q-card>
      <div class="q-pa-md ">
        <div class="text-h6">Add Job Details</div>
        <q-form class="q-gutter-sm" @submit.prevent="submitJob">
          <q-input v-model="jobId" label="Job ID" :rules="[ val => val && val.length > 0 || 'Please type something']"/>
          <!-- <q-select v-model="jobType" :options="jobTypeOptions" label="Job Type" /> -->
          <q-time v-model="selectedDateTime" mask=HH-mm label="Date and Time" now-btn />
          <div class="q-mt-md">
            <q-btn type="submit" label="Add Job" class="full-width" />
          </div>
        </q-form>
      </div>
    </q-card>
  </q-dialog>
  <q-dialog v-model="showDialog">
    <q-card>
      <div class="q-pa-md ">
        <div class="text-h6">detail</div>
        <q-form class="q-gutter-sm" @submit.prevent="submitJob">
          <q-input v-model="jobId" label="Job ID" :rules="[ val => val && val.length > 0 || 'Please type something']"/>
          <!-- <q-select v-model="jobType" :options="jobTypeOptions" label="Job Type" /> -->
          <q-time v-model="selectedDateTime" mask=HH-mm label="Date and Time" now-btn />
          <div class="q-mt-md">
            <q-btn type="submit" label="Add Job" class="full-width" />
          </div>
        </q-form>
      </div>
    </q-card>
  </q-dialog>
</template>

<script>
import {
  QCalendarMonth,
  addToDate,
  parseDate,
  parseTimestamp,
  today
} from '@quasar/quasar-ui-qcalendar/src/index.js'
import '@quasar/quasar-ui-qcalendar/src/QCalendarVariables.sass'
import '@quasar/quasar-ui-qcalendar/src/QCalendarTransitions.sass'
import '@quasar/quasar-ui-qcalendar/src/QCalendarMonth.sass'
import { defineComponent } from 'vue'
import { ref } from 'vue'
import axios from '../axios'


export default defineComponent({
  name: 'MonthSlotDay',
  components: {
    QCalendarMonth
  },
  data() {
    return {
      selectedDate: today(),
      showDialog: false,
      jobId: '',
      // jobType: null,
      // jobTypeOptions: ['Corn','interval'],
      events: [],
      des: null,
      selectedDateTime: ref(null)
    }
  },
  mounted() {
    axios.get('/get_calendar')
      .then(response => {
        this.events = response.data.map(event => {
          return {
            id: event.id,
            title:event.title,    
            date: event.date,
            time: event.time,
            details: event.details,
            bgcolor: event.bgcolor
          }
        })
      })
      .catch(error => {
        console.log(error)
      })
  },
  computed: {
    eventsMap() {
      const map = {}
      if (this.events.length > 0) {
        this.events.forEach(event => {
          (map[event.date] = (map[event.date] || [])).push(event)
          if (event.days !== undefined) {
            let timestamp = parseTimestamp(event.date)
            let days = event.days
            // add a new event for each day
            // skip 1st one which would have been done above
            do {
              timestamp = addToDate(timestamp, { day: 1 })
              if (!map[timestamp.date]) {
                map[timestamp.date] = []
              }
              map[timestamp.date].push(event)
              // already accounted for 1st day
            } while (--days > 1)
          }
        })
      }
      console.log(map)
      return map
    }
  },
  methods: {
    badgeClasses(event, type) {
      return {
        [`text-white bg-${event.bgcolor}`]: true,
        'rounded-border': true,
        
      }
    },
    onChange(data) {
      console.log('onChange', data)
    },
    onClickDate(data) {
      console.log('onClickDate', data)
      this.showDialog = true
      console.log(selectedDateTime)
    },
    onClickDay(data) {
      console.log('onClickDay', data)
    },
    onToday() {
      this.$refs.calendar.moveToToday()
    },
    onPrev() {
      this.$refs.calendar.prev()
    },
    onNext() {
      this.$refs.calendar.next()
    },
    submitJob() {
      const times = (this.selectedDate + '-' + this.selectedDateTime)
      axios.post('/schedule-job', {
        job_id: this.jobId,
        trigger_type: 'cron',
        trigger_value: times,

      }).then(response => {
        console.log(response)
        if (response.status === 201) {
          this.showDialog = false
          this.$q.notify({
            color: "positive",
            message: "save job successful",
            position: "top",
          })
        }
      })

    }



  },
})
</script>
<style lang="sass" scoped>
.my-event
  position: relative
  font-size: 12px
  width: 100%
  margin: 1px 0 0 0
  justify-content: center
  text-overflow: ellipsis
  overflow: hidden
  cursor: pointer
.rounded-border
  border-radius: 3px
</style>
