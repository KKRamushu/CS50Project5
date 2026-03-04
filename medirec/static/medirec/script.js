document.addEventListener('DOMContentLoaded', ()=>{

    //Open a list of patients with atleat one visit recorded by current doctor
    allPatientsButton = document.querySelector('#all-patients')
    myPatientsButton = document.querySelector('#my-patients')
    allPatientsNav = document.querySelector('#all-patients-nav')

    dashContainer = document.querySelector('.dash-container')
    dashDataGrid = document.querySelector('.dash-data-grid')

    // add an event listener if the "all patients button exists"
    if(allPatientsNav) {
        allPatientsNav.addEventListener('click',(e)=>{
            e.preventDefault()
            if(dashContainer){
                dashContainer.textContent = ""
                const dashOptionsDiv = new SuperElement('div',['dash-options-panel'],'')
                const dashDataPanel = new SuperElement('div',['dash-data-panel'],'')
                const newDashDataGrid = new SuperElement('div',['dash-data-grid'],'')
                allPatientsListener(newDashDataGrid)
                dashDataPanel.append(newDashDataGrid)
                
                dashContainer.append(dashOptionsDiv,dashDataPanel)
            }

        })
    }

    if(allPatientsButton) {
        allPatientsButton.addEventListener('click', (e)=>{
            e.preventDefault()
            allPatientsListener(dashDataGrid)
        })
    }

    //event listener for patients viewing buttons
    function allPatientsListener(dashDataGrid){
  
        fetch('/allPatients/')
        .then(response=>{
            if(!response.ok){
                throw new Error("Failed to fetch all patients from server")
            }
            return response.json()
        })
        .then(patients=>{
            load_patients(patients,dashDataGrid) 
        })
        .catch(error=>{console.log('Error:',error)})
    }
    

    // add an event listener if the "my patients button exists"
    if(myPatientsButton){
        myPatientsButton.addEventListener('click', (e)=>{
            e.preventDefault() //prevents "a" element default behavior
            fetch('/myPatients/')
            .then(response=> {
                if(!response.ok){
                    throw new Error("Failed to fetch my patients")  
                }
                return response.json()})
            .then(patients =>{
                load_patients(patients,dashDataGrid)
                
            })
            .catch(error=>{console.error('Error:',error)})
        })
    }
    

    // populate dashboard with patients
    function load_patients(patients,dashDataGrid){
        dashDataGrid.textContent = ''
        for(const patient of patients){
            const patientCard = new SuperElement('a',['patient-card'],'')
            const patientName = document.createElement('h4')

            patientCard.setAttribute('href',`/view_patient/${patient.user.id}`)

            patientName.textContent = `${patient.user.first_name}`

            patientCard.append(patientName)
            dashDataGrid.append(patientCard)
        }
    }

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
})