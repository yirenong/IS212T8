<template>
    <div class="container mt-4"> 
    <div v-if="$session.get('user').Dept == 'HR'">
        <div>

            <div class="row">
                <div class="col-4">
                    <div class="dropdown" @click="showDropdown">
                        <div class="overselect"></div>
                        <select class="c-form-input">
                            <option value="">Please Select One</option>
                        </select>
                    </div>
                </div>

                <div class="col-4">
                    <!-- input buttom for exactmatch -->
                    <input type="checkbox" name="exactmatch" value="exactmatch" v-model="postData.exactmatch">
                    <label for="exactmatch">ExactMatch</label>
                </div>
                <div class="col-4">
                    <button type="button" class="btn btn-primary" @click="searchfilter()">Search</button>
                </div>
            </div>
            <div class="row">
                <div class="col-4">
                    <div class="multiselect" v-if="show">
                        <ul>
                            <li v-for="skill in skill_list" :key="skill.Skill_ID">
                                <input type="checkbox" :id="skill.Skill_ID" :value="skill.Skill_ID" v-model="postData.selected">
                                <label :for="skill.Skill_ID">{{ skill.Skill_Name }}</label>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

        </div>
        <h2>Search Candidates</h2>
        <div v-if="staff_skill.length ==0"> NO DATA found</div>
        <table class="table" id="datatable" v-else >
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
        </table>
        
    </div>
    <div v-else>
        <H1 style="color:red">You are not authorized to view this page</H1>
    </div>
</div>
</template>
<style>
.col {
    flex: 0 0 50%;
    max-width: 50%;
    padding-left: 1rem;
    padding-right: 1rem;
}


/*****
- MultiSelect 
*****/

.dropdown {
    position: relative;
    cursor: pointer;
}

.multiselect {
    position: relative;

    ul {
        border: 1px solid #ddd;
        border-top: 0;
        border-radius: 0 0 3px 3px;
        left: 0px;
        padding: 8px 8px;
        position: absolute;
        top: -1rem;
        width: 100%;
        list-style: none;
        max-height: 150px;
        overflow: auto;
    }
}

.overselect {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
}
</style>
<script>

import "jquery/dist/jquery.min.js";
import "bootstrap/dist/css/bootstrap.min.css";
import "datatables.net-dt/js/dataTables.dataTables";
import "datatables.net-dt/css/jquery.dataTables.min.css";
import "datatables.net-searchpanes-dt";
import "datatables.net-searchpanes-dt/css/searchPanes.dataTables.min.css";
import "datatables.net-select-dt";
import "datatables.net-select-dt/css/select.dataTables.min.css";


import axios from "axios";
import $ from "jquery";

export default {
    mounted() {
        console.log('Component mounted.')
        console.log(this.$session.get('user'))
        if (this.$session.get('user') == null) {
            this.$router.push('/login')
        }
    },
    data() {
        return {
            selectedSkill: 'All',
            skill_list: [],
            staff_skill: [],
            filtered_staff_skill: [],
            show: false,
            postData: {
                selected: [],
                exactmatch: false
            }
        };
    },
    methods: {
        showDropdown() {
            this.show = !this.show
        },
        onChange() {
            console.log(this.selectedSkill);
            if (this.selectedSkill == 'All') {
                this.filtered_staff_skill = this.staff_skill;
            } else {
                this.filtered_staff_skill = this.staff_skill.filter(staff => staff.Skills.includes(this.selectedSkill));

            }
        },
        searchfilter() {
            axios.post('http://localhost:5000/api/search_staff_by_skill', this.postData).then(response => {
                    this.staff_skill = response.data;
                    console.log(this.staff_skill)
                    this.staff_skill.map(staff => {
                        staff.Skills.map((skill, index) => {
                            staff.Skills[index] = this.skill_list[parseInt(skill) - 1].Skill_Name;
                        });
                    });
                   
                }).then(() => {
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
                            destroy: true,
                            columns: [
                                { data: 'Staff_ID' },
                                { data: 'Staff_FName' },
                                { data: 'Dept' },
                                {
                                    data: 'Skills',
                                    render: {
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
        searchAll() {
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
                                    render: {
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
    },

};
</script>
  
  
  