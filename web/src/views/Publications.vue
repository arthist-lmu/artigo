<template>
  <v-simple-table id="publications">
      <template v-slot:default>
      <thead>
          <tr>
          <th class="text-left">
              Name
          </th>
          </tr>
      </thead>
      <tbody>
          <tr
          v-for="item in publications"
          :key="item.name"
          >
          <td>{{ item.name }}</td>
          </tr>
      </tbody>
      </template>
  </v-simple-table>
</template>

<script>
export default {
  data() {
    return {
      publications: [
        {
          name: `
                Bry, François, Schefels, Clemens und Schemainda, Corina (2018):
                „Eine qualitative Analyse der ARTigo-Annotationen“,
                in: Kuroczyński, Piotr, Bell, Peter und Dieckmann, Lisa (Hrsg.):
                Computing Art Reader. Einführung in die digitale Kunstgeschichte, S. 96–114",
              `,
          calories: 159,
        },
        {
          name: 'Ice cream sandwich',
          calories: 237,
        },
        {
          name: 'Eclair',
          calories: 262,
        },
        {
          name: 'Cupcake',
          calories: 305,
        },
        {
          name: 'Gingerbread',
          calories: 356,
        },
        {
          name: 'Jelly bean',
          calories: 375,
        },
        {
          name: 'Lollipop',
          calories: 392,
        },
        {
          name: 'Honeycomb',
          calories: 408,
        },
        {
          name: 'Donut',
          calories: 452,
        },
        {
          name: 'KitKat',
          calories: 518,
        },
      ],
    };
  },
};
</script>
