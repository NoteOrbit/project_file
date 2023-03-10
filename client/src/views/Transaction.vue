<template>
  <div class="q-px-lg q-pb-md">

        <q-intersection
        :key="index"
        transition="jump-down"
      >
    <q-timeline :layout="layout" color="secondary">
      <q-timeline-entry heading>
        Timeline Progress
        <br>
      </q-timeline-entry>

      <q-timeline-entry
        title="Research Informations"
        subtitle="February 22, 1986"
        side="left"
      >
        <div>
          A
        </div>
      </q-timeline-entry>

      <q-timeline-entry
        title="Experimental Model"
        subtitle="February 21, 1986"
        side="right"
      >
        <div>
          B
        </div>
      </q-timeline-entry>

      <q-timeline-entry heading>March, 2022</q-timeline-entry>

      <q-timeline-entry
        title="Implement project"
        subtitle="February 22, 1986"
        side="left"
        color="orange"
      >
        <div>
          C
        </div>
      </q-timeline-entry>
      <q-timeline-entry
        title="Test project"
        subtitle="February 22, 1986"
        side="right"
        color="orange"
      >
        <div>
          X
        </div>
      </q-timeline-entry>
      <q-timeline-entry
        title="Final project"
        subtitle="February 22, 1986"
        side="left"
        color="green"
        icon="done"
      >
        <div>
          Final project
        </div>
      </q-timeline-entry>


    </q-timeline>
    </q-intersection>
  </div>
</template>

<script>
import { useQuasar } from 'quasar'
import { computed } from 'vue'

export default {
  setup () {
    const $q = useQuasar()

    return {
      layout: computed(() => {
        return $q.screen.lt.sm ? 'dense' : ($q.screen.lt.md ? 'comfortable' : 'loose')
      })
    }
  }
}
</script>
