<template>
  <div class="time-selector">
    <label for="date" class="form-label">Date:</label>
    <div class="input-group">
      <select class="form-select" v-model="selectedYear" @change="updateDate">
        <option v-for="year in years" :key="year" :value="year">
          {{ year }}
        </option>
      </select>
      <select class="form-select" v-model="selectedMonth" @change="updateDate">
        <option
          v-for="(month, index) in months"
          :key="index"
          :value="index + 1"
        >
          {{ month }}
        </option>
      </select>
      <select class="form-select" v-model="selectedDay" @change="updateDate">
        <option v-for="day in daysInMonth" :key="day" :value="day">
          {{ day }}
        </option>
      </select>
    </div>
  </div>
</template>

<script>
export default {
  name: "TimeSelector",
  data() {
    return {
      selectedYear: new Date().getFullYear(),
      selectedMonth: new Date().getMonth() + 1,
      selectedDay: new Date().getDate(),
    };
  },
  computed: {
    years() {
      const currentYear = new Date().getFullYear();
      return Array.from({ length: 20 }, (_, i) => currentYear - i);
    },
    months() {
      return [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ];
    },
    daysInMonth() {
      return Array.from(
        {
          length: new Date(this.selectedYear, this.selectedMonth, 0).getDate(),
        },
        (_, i) => i + 1
      );
    },
  },
  methods: {
    updateDate() {
      const daysInSelectedMonth = new Date(
        this.selectedYear,
        this.selectedMonth,
        0
      ).getDate();
      if (this.selectedDay > daysInSelectedMonth) {
        this.selectedDay = daysInSelectedMonth;
      }

      const selectedDate = `${this.selectedYear}-${String(
        this.selectedMonth
      ).padStart(2, "0")}-${String(this.selectedDay).padStart(2, "0")}`;
      this.$emit("date-selected", selectedDate);
    },
  },
};
</script>

<style scoped>
.time-selector {
  margin-bottom: 1rem;
}
</style>
