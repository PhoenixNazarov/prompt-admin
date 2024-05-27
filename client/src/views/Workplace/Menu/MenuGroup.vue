<script lang="ts">
import {defineComponent} from 'vue'
import logoExpand from '../../../assets/expand_more.svg'

export default defineComponent({
  name: 'MenuGroup',
  props: {
    name: {
      type: String,
      required: true
    },
    startOpen: {
      type: Boolean,
      default: true
    },
    disabled: {
      type: Boolean,
      default: false
    },
    bold: {
      type: Boolean,
      default: false
    },
    center: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      logoExpand: logoExpand,
      open: this.startOpen,
      observer: undefined as ResizeObserver | undefined
    }
  },
  methods: {
    openCloseGroup() {
      this.open = !this.open
      this.reorganize()
    },
    reorganize() {
      const content = this.$refs['close-content'] as HTMLDivElement
      const contentHeight = this.$refs['close-content-height'] as HTMLDivElement
      const button = this.$refs['close-button'] as HTMLDivElement
      if (content) {
        if (this.open && !this.disabled) {
          content.style.height = `${contentHeight.scrollHeight}px`
          button.style.transform = 'rotate(0deg)'
        } else {
          content.style.height = '0'
          button.style.transform = 'rotate(-90deg)'
        }
      }
    }
  },
  mounted() {
    const contentHeight = this.$refs['close-content-height'] as HTMLDivElement
    this.observer = new ResizeObserver(this.reorganize)
    this.observer.observe(contentHeight)
    this.reorganize()
  },
  updated() {
    this.$nextTick().then(this.reorganize)
  }
})
</script>

<template>
  <div>
    <div class="group-name">
      <div class="title" :class="disabled ? '' : 'pointer'" :style="center ? '    align-items: flex-start;' : ''"
           @click.prevent="openCloseGroup">
        <img
            class="expand-image"
            :class="disabled ? 'disable' : ''"
            :src="logoExpand"
            ref="close-button"
        />
        <div
            class="group-title"
            :class="[disabled ? 'disable' : '', bold ? 'bold': '']"
            :style="center ? '    line-height: normal;' : ''"
        >
          {{ name }}
        </div>
      </div>
    </div>
    <div class="group-content" ref="close-content">
      <div ref="close-content-height">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<style scoped>
.group-name {
  display: flex;
  align-items: center;
}

.expand-image {
  width: 2rem;
  transition: 500ms;
}

.group-title {
  font-size: 1.25rem;
  font-style: normal;
  font-weight: 500;
}

.group-content {
  overflow: hidden;
  transition: height 500ms;
}

.title {
  display: flex;
  align-items: center;
}

.bold {
  text-transform: uppercase;
  font-weight: 800;
}
</style>
