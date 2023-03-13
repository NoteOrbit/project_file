<template>
  <div class="q-pa-md q-gutter-sm row justify-center">
    <q-btn @click=onNext style="background: black; color: white" label="Next" />
    <q-btn @click=onToday outline style="color: green" label="To Day" />
    
  </div>
  <q-dialog v-model="displayEvent">
      <div>
        <q-card v-if="event">
          <q-toolbar :class="displayClasses(event)"  style="min-width: 400px;">
            <q-toolbar-title>
              {{ event.title }}
            </q-toolbar-title>
            <q-btn flat round color="white" icon="delete" v-close-popup @click="deleteEvent(event)"></q-btn>
            <q-btn flat round color="white" icon="edit" v-close-popup @click="editEvent(event)"></q-btn>
            <q-btn flat round color="white" icon="close" v-close-popup></q-btn>
          </q-toolbar>
          <q-card-section class="inset-shadow">
            <div v-if="event.allDay" class="text-caption">{{ getEventDate(event) }}</div>
            {{ event.details }}
            <div v-if="event.time" class="text-caption">
              <div class="row full-width justify-start" style="padding-top: 12px;">
                <div class="col-12">
                  <div class="row full-width justify-start">
                    <div class="col-5" style="padding-left: 20px;">
                      <strong>Start Time:</strong>
                    </div>
                    <div class="col-7">
                      {{ event.time }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </q-card-section>
          <q-card-actions align="right">
            <q-btn flat label="OK" color="primary" v-close-popup></q-btn>
          </q-card-actions>
        </q-card>
      </div>
    </q-dialog>
  <div class="row justify-center">
    <div style="display: flex; justify-content: center; align-items: center; flex-wrap: nowrap;">
    </div>
    <div style="display: flex; max-width: 800px; width: 100%;">
      <q-calendar-month 
      
      ref="calendar"
      v-model="selectedDate"
      animated 
      bordered 
      focusable
      hoverable
      use-navigation
      no-active-date
      :day-min-height="60"
      :day-height="0"
      @click-date="onClickDate" 
      @click-day="onClickDay" 
      >
       
      <template #day="{ scope: { timestamp } }">
          
          <template v-for="event in eventsMap[timestamp.date]" :key="event.id">
              <q-badge
                
                style="width: 100%; cursor: pointer; height: 14px; max-height: 14px"
                :class="badgeClasses(event, 'day')"
                :style="badgeStyles(event, 'day')"
                @click.stop.prevent="showEvent(event)"
              >
                <q-icon v-if="event.icon" :name="event.icon" class="q-mr-xs"></q-icon><span class="ellipsis">{{ event.title }}</span>
                <q-tooltip>{{ event.time }}</q-tooltip>
              </q-badge>
            </template>
          </template>
        
      </q-calendar-month>
    </div>
  </div>
  <q-dialog v-model="showDialog">
    <q-card>
      

        <q-form class="q-gutter-sm" @submit.prevent="submitJob">
          <q-toolbar class="bg-green text-white">
          <q-toolbar-title >
                Add job detail
              </q-toolbar-title>
            </q-toolbar>
            <q-card-section>
          <q-input v-model="jobId" label="Job ID" :rules="[ val => val && val.length > 0 || 'Please type something']"/>
          
          <q-time color='green' v-model="selectedDateTime" mask=HH-mm label="Date and Time" now-btn landscape />
          <div class="q-mt-md">
            <q-btn type="submit" label="Add Job" class="full-width" />
          </div>
        </q-card-section>
        </q-form>
      
    </q-card>
  </q-dialog>

     
    <!-- add/edit an event -->
    <q-dialog v-model="addEvent" no-backdrop-dismiss>
      <div>
        <q-form
          v-if="contextDay"
          ref='event'
          @submit="onSubmit"
          @reset="onReset"
        >
          <q-card v-if="addEvent" >
            <q-toolbar class="bg-green text-white">
              <q-toolbar-title>
                Job Modify
              </q-toolbar-title>
              <q-btn flat round color="white" icon="close" v-close-popup></q-btn>
            </q-toolbar>
            <q-card-section class="inset-shadow">
              <q-input
                v-model="eventForm.title"
                label="Title"
                :rules="[v => v && v.length > 0 || 'Field cannot be empty']"
                autofocus
                disable
              />
              <q-time v-model="eventForm.details" color="green" mask=HH-mm label="Date and Time" now-btn landscape />

            </q-card-section>
            <q-card-actions align="right">
              <q-btn flat label="OK" type="submit" color="primary"></q-btn>
              <q-btn flat label="Cancel" type="reset" color="primary" v-close-popup></q-btn>
            </q-card-actions>
          </q-card>
        </q-form>
      </div>
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
import QCalendar from '@quasar/quasar-ui-qcalendar'
import '@quasar/quasar-ui-qcalendar/src/QCalendarVariables.sass'
import '@quasar/quasar-ui-qcalendar/src/QCalendarTransitions.sass'
import '@quasar/quasar-ui-qcalendar/src/QCalendarMonth.sass'
import { defineComponent } from 'vue'
import { ref, computed } from 'vue'
import axios from '../axios'


const formDefault = {
  title: '',
  details: '',

}

export default defineComponent({
  name: 'MonthSlotDay',
  components: {
    QCalendarMonth
  },
  setup () {
    const moreContent = ref(true)

    return {
      layout: ref(false),

      moreContent,
      contentSize: computed(() => moreContent.value ? 150 : 5),
      drawer: ref(false),
      drawerR: ref(false),

      lorem: 'Lorem ipsum dolor sit amet consectetur, adipisicing elit. Natus, ratione eum minus fuga, quasi dicta facilis corporis magnam, suscipit at quo nostrum!'
    }
  },


  data() {
    return {
      selectedDate: today(),
      showDialog: false,
      jobId: '',
      displayEvent: false,
      addEvent: false,
      eventForm: { ...formDefault },
      // jobType: null,
      // jobTypeOptions: ['Corn','interval'],
      events: [],
      event: null,
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
            title: event.title,
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

            do {
              timestamp = addToDate(timestamp, { day: 1 })
              if (!map[timestamp.date]) {
                map[timestamp.date] = []
              }
              map[timestamp.date].push(event)

            } while (--days > 1)
          }
        })
      }
      console.log(map)
      return map
    }
  },
  methods: {
      resetForm () {
      this.$set(this, 'eventForm', { ...`formDefault` })
    },
    displayClasses (event) {
      return {
        [`text-white bg-${event.bgcolor}`]: true,
        'rounded-border': true
      }
    },
    onSubmit () {
      this.saveEvent()
    },

    onReset () {

    },

      saveEvent () {
        const self = this
        this.$refs.event.validate().then((success) => {
          if (success) {
            // close the dialog
            self.addEvent = false
            const form = { ...self.eventForm }
            let update = false
            if (self.contextDay.bgcolor) {
              // an update
              update = true
            }
            else {
              // an add
            }
            const data = {
              title: form.title,
              details: form.details,
              
            }
            if (form.allDay === false) {
              // get time into separate var
              data.time = String(form.dateTimeStart).slice(11, 16)
              data.duration = self.getDuration(form.dateTimeStart, form.dateTimeEnd, 'minutes')
            }
            if (update === true) {
              const index = self.findEventIndex(self.contextDay)
              if (index >= 0) {
                self.events.splice(index, 1, { ...data })
              }
            }
            else {
              // add to events array
              self.events.push(data)
            }

            self.contextDay = null
          }
        })
      },
    editEvent (event) {
      const form = { ...self.eventForm }
      console.log(form)
      // this.resetForm()
      this.contextDay = { ...event }
      console.log(this.contextDay)
      let timestamp
      if (event.time) {
        
        timestamp = QCalendar.parseTimestamp(event.date + ' ' + event.time)
        
        
      }
      else {
        timestamp = QCalendar.parseTimestamp(this.contextDay.date + ' 00:00')
        console.log('asdasdas')
      }
      
      this.eventForm.title = event.title
      this.eventForm.details = event.details
      this.addEvent = true // show dialog
    },
    deleteEvent (event) {
      const index = this.findEventIndex(event)
      

    if (event['id'] === 'my_job') {
      this.$q.notify({
            color: "negative",
            message: "can't delate interval job you can turn off job below buttom",
            position: "top",
          })
    }else {
      axios.post('/remove_job',{"id":event['id']})    
      if (index >= 0) {
        this.events.splice(index, 1)
       }
       this.$q.notify({
            color: "negative",
            message: "Job delate id "+ event['id'] + ' successful',
            position: "top",
          })
    }


      
    },
    findEventIndex (event) {
      for (let i = 0; i < this.events.length; ++i) {
        if (event.title === this.events[i].title &&
          event.details === this.events[i].details &&
          event.date === this.events[i].date) {
          return i
        }
      }
    },
    badgeClasses(event, type) {
      return {
        [`text-white bg-${event.bgcolor}`]: true,
        'rounded-border': true
      }
    },
    badgeStyles(day, event) {
      const s = {}
      s.left = day.weekday === 0 ? 0 : (day.weekday * this.parsedCellWidth) + '%'
      s.top = 0
      s.bottom = 0
      return s
    },
    showEvent (event) {
      
      
        this.event = event
        this.displayEvent = true
      
    },
    getEventDate (event) {
      const parts = event.date.split('-')
      const date = new Date(parts[0], parts[1] - 1, parts[2])
      return this.dateFormatter.format(date)
    },
    onClickCalendar (data) {
      console.log('Clicked calendar:', data)
    },

    onChange(data) {
      console.log('onChange', data)
    },
    clickContent(data) {
      console.log('clickContent', data)
    },
    resourceClicked ({ scope, event }) {
      console.log('resource clicked:', scope)
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
.title
  position: relative
  display: flex
  justify-content: center
  align-items: center
  height: 100%
.text-white
  color: white
.rounded-border
  border-radius: 2px
</style>
