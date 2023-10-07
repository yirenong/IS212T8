<template>
    <div v-if="$session.get('user').Dept == 'HR'">
        <h2>Search Candidates</h2>
        <!-- select to filter  -->
        <!-- <select v-model="selectedSkill" @change="onChange($event)">
            <option value="All">All</option>
            <option v-for="(skill, index) in skill_list" :key="index" :value="skill.Skill_ID">
                {{ skill.Skill_Name }}
            </option>
        </select> -->


        <table class="table" id="datatable">
            <thead>
                <tr>
                    <th>Staff ID</th>
                    <th>Staff Name</th>
                    <th> Department</th>
                    <th>Staff Skills</th>
                </tr>
            </thead>
            <tfoot>
                <tr>
                    <th>Staff ID</th>
                    <th>Staff Name</th>
                    <th> Department</th>
                    <th>Staff Skills</th>
                </tr>
            </tfoot>
            <!--<tbody>
                <tr v-for="(staff, index) in staff_skill" :key="index">
                    <td>{{ staff.Staff_ID }}</td>
                    <td>{{ staff.Staff_FName + staff.Staff_LName }}</td>
                    <td>{{ staff.Dept }}</td>
                    <td>
                        <ul>
                            <li v-for="(skill, skillIndex) in staff.Skills" :key="skillIndex">
                                {{ skill_list[parseInt(skill) - 1].Skill_Name }}
                            </li>
                        </ul>
                    </td>
                </tr>
            </tbody> -->
        </table>
    </div>
    <div v-else>
        <H1 style="color:red">You are not authorized to view this page</H1>
    </div>
</template>
  
<script>

import "jquery/dist/jquery.min.js";
import "bootstrap/dist/css/bootstrap.min.css";
import "datatables.net-dt/js/dataTables.dataTables";
import "datatables.net-dt/css/jquery.dataTables.min.css";
import "datatables.net-searchpanes-dt";
import "datatables.net-searchpanes-dt/css/searchPanes.dataTables.min.css";
import "datatables.net-select-dt";
import "datatables.net-select-dt/css/select.dataTables.min.css";
// impo


import axios from "axios";
import $ from "jquery";

export default {
    mounted() {
        console.log('Component mounted.')
        console.log(this.$session.get('user'))
        if (this.$session.get('user') ==  null) {
            this.$router.go(0);
        }
    },
    data() {
        return {
            selectedSkill: 'All',
            skill_list: [],
            staff_skill: [],
            filtered_staff_skill: [],
        };
    },
    methods: {
        onChange() {
            console.log(this.selectedSkill);
            if (this.selectedSkill == 'All') {
                this.filtered_staff_skill = this.staff_skill;
            } else {
                this.filtered_staff_skill = this.staff_skill.filter(staff => staff.Skills.includes(this.selectedSkill));

            }
        }
    },
    created() {
        
        axios.get('http://localhost:5000/api/skill_list')
            .then(response => {
                this.skill_list = response.data;
                console.log('Job Listings:', this.skill_list);
            })
            .catch(error => {
                console.error('Error fetching job listings:', error);
            });
        axios.get('http://localhost:5000/api/staff_skill')
            .then(response => {
                this.staff_skill = response.data;

                this.staff_skill.map(staff => {
                    staff.Skills.map((skill, index) => {
                        staff.Skills[index] = this.skill_list[parseInt(skill) - 1].Skill_Name;
                    });
                });
                // Write DataTable to filter by dropdown by column
                $('#datatable tfoot th').each(function () {
                    var title = $(this).text();
                    $(this).html('<input type="text" placeholder="Search ' + title + '" />');
                });

                $("#datatable").DataTable(
                    {
                        searchPanes: {
                            viewTotal: true
                        },
                        dom: 'Plfrtip',
                        data: this.staff_skill,
                        columns: [
                            { data: 'Staff_ID' },
                            { data: 'Staff_FName' },
                            { data: 'Dept' },
                            {
                                data: 'Skills',
                                render:{
                                    _: '[,]',
                                    sp: '[]'
                                },
                                searchPanes: {
                                    orthogonal: 'sp'
                                }
                            }
                        ]
                    }
                ).columns().every(function () {
                    var that = this;

                    $('input', this.footer()).on('keyup change', function () {
                        if (that.search() !== this.value) {
                            that
                                .search(this.value)
                                .draw();
                        }
                    });
                });

                console.log('staff_skill Listings:', this.staff_skill);
            })
            .catch(error => {
                console.error('Error fetching candidate listings:', error);
            });


    },
};
</script>
  
  
  