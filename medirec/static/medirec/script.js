document.addEventListener('DOMContentLoaded', ()=>{

    // Element Constructor Function
    function SuperElement(type,classes,id){ //classes must be a list
        this.element = document.createElement(type)
        for(const clss of classes){
            this.element.classList.add(clss)
        }
        if(id != ''){
            this.element.setAttribute('id',id)
        }
        return this.element
    }

    //Open a list of patients with atleat one visit recorded by current doctor
    allPatientsButton = document.querySelector('#all-patients')
    myPatientsButton = document.querySelector('#my-patients')
    allPatientsNav = document.querySelector('#all-patients-nav')

    dashContainer = document.querySelector('.dash-container')
    dashDataPanel = document.querySelector('.dash-data-panel')
    dashDataGrid = document.querySelector('.dash-data-grid')

    dashContainer.addEventListener('click',function(e){
        // add an event listener if the "all patients button exists"
        if(e.target.matches("#all-patients")){
            e.preventDefault()//prevents "a" element default behavior
            allPatientsListener(dashDataPanel)
        }

        // add an event listener if the "my patients button exists"
        if(e.target.matches("#my-patients")){
            e.preventDefault() //prevents "a" element default behavior
            fetch('/myPatients/')
            .then(response=> {
                if(!response.ok){
                    throw new Error("Failed to fetch my patients")  
                }
                return response.json()})
            .then(patients =>{
                load_patients(patients,dashDataPanel)
                
            })
            .catch(error=>{console.error('Error:',error)})
        }
    })

    //event listener for patients viewing buttons
    function allPatientsListener(dashDataPanel){
  
        fetch('/allPatients/')
        .then(response=>{
            if(!response.ok){
                throw new Error("Failed to fetch all patients from server")
            }
            return response.json()
        })
        .then(patients=>{
            load_patients(patients,dashDataPanel) 
        })
        .catch(error=>{console.log('Error:',error)})
    } 

    // populate dashboard with patients
    function load_patients(patients,dashDataPanel){
        dashDataPanel.textContent = ''
        const newDashDataGrid = new SuperElement('div',['dash-data-grid'],'')
        for(const patient of patients){
            const patientCard = new SuperElement('a',['patient-card'],'')
            const patientName = document.createElement('h4')

            patientCard.setAttribute('href',`/view_patient/${patient.user.id}`)

            patientName.textContent = `${patient.user.first_name}`

            patientCard.append(patientName)
            newDashDataGrid.append(patientCard)
        }
        dashDataPanel.append(newDashDataGrid)
    }

})
