<template>
  <div class="card p-3">
    <div class="mb-3">
      <label for="nameInput" class="form-label">name</label>
      <input
        type="text"
        id="nameInput"
        class="form-control"
        v-model="localRecord.name"
      />
    </div>

    <div class="mb-3">
      <label for="amountInput" class="form-label">amount</label>
      <input
        type="number"
        min="0"
        id="amountInput"
        class="form-control"
        v-model="localRecord.amount"
      />
    </div>

    <div class="mb-0">
      <label class="form-label">tags</label>
    </div>

    <div class="mb-3 d-flex flex-wrap">
      <div
        class="form-check me-3 mb-2"
        v-for="(tag, index) in mergedTags"
        :key="index"
      >
        <input
          class="form-check-input"
          type="checkbox"
          :id="'checkbox-' + index"
          v-model="localRecord.selectedTags"
          :value="tag"
        />
        <label class="form-check-label" :for="'checkbox-' + index">
          {{ tag }}
        </label>
      </div>
      <button class="btn btn-primary btn-sm" @click="addTag">+</button>
    </div>

    <div class="mx-auto">
      <button class="btn btn-danger me-2" @click="submit('expense')">
        expense
      </button>
      <button class="btn btn-success me-2" @click="submit('income')">
        income
      </button>
    </div>
  </div>
</template>

<script>
import { useAuth } from "@/useAuth";
import axios from "axios";
import { toast } from "vue3-toastify";

export default {
  setup() {
    const { userInfo } = useAuth();

    return {
      userInfo,
    };
  },
  props: {
    record: {
      type: Object,
      default: () => ({
        name: "",
        amount: 0,
        tags: [],
        type: "",
        date: "",
      }),
    },
  },
  data() {
    return {
      defaultTags: [
        "Food",
        "Clothing",
        "Housing",
        "Transportation",
        "Education",
        "Entertainment",
      ],
      localRecord: {
        record_id: "",
        name: "",
        amount: 0,
        selectedTags: [],
        type: "",
        date: "",
      },
    };
  },
  computed: {
    mergedTags() {
      return [
        ...new Set([...this.defaultTags, ...this.localRecord.selectedTags]),
      ];
    },
  },
  watch: {
    record: {
      immediate: true,
      handler(newRecord) {
        this.localRecord = { ...newRecord, selectedTags: [...newRecord.tags] };
      },
    },
    "localRecord.selectedTags": {
      handler(newTags) {
        newTags.forEach((tag) => {
          if (!this.defaultTags.includes(tag)) {
            this.defaultTags.push(tag);
          }
        });
      },
      deep: true,
    },
  },
  methods: {
    addTag() {
      const newTag = prompt("Input new tag:");
      if (newTag && !this.defaultTags.includes(newTag)) {
        this.defaultTags.push(newTag);
      }
    },
    submit(type) {
      if (!this.localRecord.amount || isNaN(this.localRecord.amount)) {
        alert("Please enter a valid number for the amount.");
        return;
      }

      this.localRecord.type = type;
      this.localRecord.date = new Date().toISOString();

      const payload = {
        userId: this.userInfo.sub,
        records: [
          {
            name: this.localRecord.name,
            amount: this.localRecord.amount,
            tags: this.localRecord.selectedTags,
            type: this.localRecord.type,
            date: this.localRecord.date,
          },
        ],
      };

      this.localRecord.record_id = this.$route.query.record_id;

      const url = this.localRecord.record_id
        ? `http://localhost:5000/api/update/record`
        : "http://localhost:5000/api/add/record";

      const method = this.localRecord.record_id ? "put" : "post";

      axios[method](
        url,
        this.localRecord.record_id
          ? {
              userId: this.userInfo.sub,
              record_id: this.localRecord.record_id,
              record: payload.records[0],
            }
          : payload
      )
        .then((res) => {
          console.log("Data saved:", res.data);
          console.log(payload);

          toast(`${payload.records[0].name} $ ${payload.records[0].amount}`, {
            theme: "colored",
            type: payload.records[0].type === "income" ? "success" : "error",
            position: "top-center",
            pauseOnFocusLoss: false,
            dangerouslyHTMLString: true,
          });
        })
        .catch((err) => {
          console.error("Error saving data:", err);
        });

      if (this.$route.name === "RecordPage") {
        this.cleanForm();
      } else if (this.$route.name === "EditPage") {
        this.$router.push({ name: "HistoryPage" });
      }
    },
    cleanForm() {
      this.localRecord = {
        name: "",
        amount: 0,
        selectedTags: [],
        type: "",
        date: "",
      };
    },
  },
};
</script>

<style scoped>
.container {
  padding-top: 20px;
}
.chart-container {
  position: relative;
  height: 200px;
  width: 100%;
}
</style>
