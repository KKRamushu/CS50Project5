document.addEventListener('DOMContentLoaded', ()=>{

    // Element Constructor Function
    class SuperElement{
        constructor(type,classes,id){ //classes must be a list
            this.element = document.createElement(type)
            if(Array.isArray(classes)){
                for(const clss of classes){
                    this.element.classList.add(clss)
                }
            }
            if(id){
                this.element.id = id
            }
        }

        detail(lable,value){
            let lableWrap = document.createElement('div')
            let valueWrap = document.createElement('div')

            let detailLable= document.createElement('strong')
            let detailValue= document.createElement('small')

            lableWrap.classList.add('detail-lable')
            valueWrap.classList.add('detail-value')

            detailLable.textContent = lable
            detailValue.textContent = value

            lableWrap.append(detailLable)
            valueWrap.append(detailValue)

            this.element.append(lableWrap,valueWrap)

        }
    }

    //Open a list of patients with atleat one visit recorded by current doctor
    allPatientsButton = document.querySelector('#all-patients')
    myPatientsButton = document.querySelector('#my-patients')
    allPatientsNav = document.querySelector('#all-patients-nav')

    dashContainer = document.querySelector('.dash-container')
    dashDataPanel = document.querySelector('.dash-data-panel')
    dashDataGrid = document.querySelector('.dash-data-grid')

    patientInfoPanel = document.querySelector('#patient-info-panel')
    patientVisitForm = document.querySelector('#new-visit-form')
    patientVisitDetails = document.querySelector('#patient-visit-details')

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
            patientName = document.createElement('h4')

            patientCard.element.setAttribute('href',`/view_patient/${patient.user.id}`)

            patientName.textContent = `${patient.user.first_name}`

            patientCard.element.append(patientName)
            newDashDataGrid.element.append(patientCard.element)
        }
        dashDataPanel.append(newDashDataGrid.element)
    }

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

        //add patient info listener
        if(e.target.matches("#patient-info")){
            e.preventDefault()
            patientId = e.target.dataset.patientId
            dashDataPanel.textContent = ''

            fetch(`/patient_info/${patientId}`)
            .then(response=>{
                if(!response.ok){throw new Error("failed to fetch patient info")}
                return response.json()
            })
            .then(info=>{

                patientDetailsContainer = new SuperElement('div',['patient-details-container'],'')
                heading = new SuperElement('h4',[],'')
                heading.textContent = 'Personal details'

                nameDiv = new SuperElement('div',['details'],'')
                nameDiv.detail('Name',`${info.user.first_name} ${info.user.last_name}`)
                nameDiv = nameDiv.element

                idDiv = new SuperElement('div',['details'],'')
                idDiv.detail('ID',info.patient_id)
                idDiv = idDiv.element

                phoneNumber = new SuperElement('div',['details','patient-detail'],'')
                phoneNumber.detail('Contact',info.contact)
                phoneNumber = phoneNumber.element
                email = new SuperElement('div',['details','patient-detail'],'')
                email.detail('Email',info.user.username)
                email = email.element
                patientAddress = new SuperElement('div',['details','patient-detail'],'') 
                patientAddress.detail('Address',info.address)
                patientAddress = patientAddress.element

                detailsContainer1 = new SuperElement('div',['details-container'],'')
                detailsContainer1 = detailsContainer1.element
                detailsContainer1.append(phoneNumber,email,patientAddress)

                gender = new SuperElement('div',['details','patient-detail'],'')
                gender.detail('Gender :',info.gender)
                gender =gender.element
                bloodType = new SuperElement('div',['details','patient-detail'],'')
                bloodType.detail('Blood Type :', info.blood_type)
                bloodType = bloodType.element

                detailsContainer2 = new SuperElement('div',['details-container'],'')
                detailsContainer2 = detailsContainer2.element
                detailsContainer2.append(gender,bloodType)

                allergies = new SuperElement('div',['details'],'')
                allergies.detail('Allegies :', info.allergies)
                allergies = allergies.element

                patientDetailsContainer.element.append(heading.element,nameDiv,idDiv,detailsContainer1,detailsContainer2,allergies)
                dashDataPanel.append(patientDetailsContainer.element)

            })
        }

        if(e.target.matches('#patient-visits')){
            e.preventDefault()
            patientId = e.target.dataset.patientId

            fetch(`/visits/${patientId}`)
            .then(response=>{
                if(!response.ok){throw new Error("failed to fetch patient's visits")}
                return response.json()
            })
            .then(visits=>{
                dashDataPanel.textContent = ''
                heading = new SuperElement('h4',[],'')
                heading = heading.element
                heading.textContent = 'Patient Visits'

                visitsTable = new SuperElement('table',['visit-details-container','visits-table'], '')
                visitsTable = visitsTable.element

                tableHead = new SuperElement('thead',['table-head'],'')
                tableHead = tableHead.element
                th1 = new SuperElement('th',[],'')
                th2 = new SuperElement('th',[],'')
                th3 = new SuperElement('th',[],'')
                th1.element.textContent = 'Reason for Visit'
                th2.element.textContent = 'Date'
                th3.element.textContent = 'Doctor'
                tableHead.append(th1.element,th2.element,th3.element)

                tableBody = new SuperElement('tbody',['table-body'],'')
                tableBody =tableBody.element
                for(const visit of visits){
                
                    tableRow = new SuperElement('tr',['details','patient-visit'],'')
                    tableRow = tableRow.element
                    tableRow.setAttribute('data-visit-id',visit.visitId)
                    tableData1 = new SuperElement('td',[])
                    tableData2 = new SuperElement('td',[])
                    tableData3 = new SuperElement('td',[])
                    tableData1.element.textContent = visit.reason
                    tableData2.element.textContent = visit.visit_date
                    tableData3.element.textContent = visit.doctor.doctorName

                    tableRow.append(tableData1.element,tableData2.element,tableData3.element)
                    tableBody.append(tableRow)
                }
                visitsTable.append(tableHead,tableBody)
                dashDataPanel.append(heading,visitsTable)

            })
        }
        //EventListener for patient visit
        if(e.target.matches('.patient-visit')){
            visitId = e.target.dataset.visitId
            fetch(`/viewVisit/${visitId}`)
            .then(response=>{
                if(!response.ok){throw new Error("Failed to fetch Visit details")}
                return response.json()
            })
            .then(visit=>{
            
                visitDetailsContainer = new SuperElement('div',['visit-details-container'],'')
                visitDetailsContainer = visitDetailsContainer.element

                dashDataPanel.textContent = ''
                heading = new SuperElement('h4',[],'')
                heading = heading.element
                heading.textContent = 'Patient Visit Details'

                reason = new SuperElement('div',['visit-details'],'')
                reason.detail('Reason For Visit :',visit.visit.reason)
                reason = reason.element
                
                vitalsContainer = new SuperElement('div',['vital-details-container'],'')
                vitalsContainer = vitalsContainer.element

                bp = new SuperElement('div',['details','vital-details'],'')
                bp.detail('BP :', visit.blood_pressure)
                bp = bp.element
                temp = new SuperElement('div',['details','vital-details'],'')
                temp.detail('Temp :', visit.temperature)
                temp = temp.element
                pulse = new SuperElement('div',['details','vital-details'],'')
                pulse.detail('Pulse :', visit.heart_rate)
                pulse = pulse.element

                vitalsContainer.append(bp,temp,pulse)

                diagnosis = new SuperElement('div',['visit-details'],'')
                diagnosis.detail('Diagnosis :',visit.visit.diagnostic)
                diagnosis = diagnosis.element

                treatment = new SuperElement('div',['visit-details'],'')
                treatment.detail('Treatment :',visit.visit.treatment)
                treatment = treatment.element

                notes = new SuperElement('div',['visit-details'],'')
                notes.detail('Notes :',visit.visit.notes)
                notes = notes.element

                visitDetailsContainer.append(heading,reason,vitalsContainer,diagnosis,treatment,notes)
                dashDataPanel.append(visitDetailsContainer)
                console.log(dashDataPanel)
                alert(dashDataPanel)
            })
        }
    })

})
