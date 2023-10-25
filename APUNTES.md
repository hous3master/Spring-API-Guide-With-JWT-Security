## Setup

### Spring

Permitir CORS en el controller de la entidad:

##### miEntidadController.java
```java
// Default imports
// ...
@RestController
@CrossOrigin(origins = "http://localhost:4200") // Allow CORS
@RequestMapping("/miEntidad")
// ...
```

### Angular

Escribir en la terminal `ng new nombremiEntidad`. Y usar la siguiente configuración:

Prompt | Respuesta
---|---
`? Would you like to add Angular routing?` | Yes
`? Which stylesheet format would you like to use?`  | CSS

Alocar la terminal en el miEntidad con el comando `cd miProyecto`

### Dependencies

#### Angular Material

Agregar angular material al miEntidad, mediante la consola `ng add @angular/material`. Y usar la siguiente configuración:

Prompt | Respuesta
---|---
`? Would you like to share pseudonymus data...`| No
`? Choose a prebuilt theme name, or "custom" for a custom theme:` | Indigo/Pink
`? Set up global Angular Material typography styles?` | Yes
`? Set up browser animations for Angular Material?` | Yes

#### Moment

Agregar moment al miEntidad, mediante la consola `ng add moment`

### Bootstrap

Agregar a archivo `index.html`, antes de `</head>` tag.

##### index.html
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
```

## Enviroments

En `nombremiEntidad` crear folder `enviroments`.

En `nombremiEntidad/enviroments` crear un archivo `enviroment.ts` con el siguiente contenido:

##### enviroment.ts
```typescript
export const enviroment = {
  production: false,
  base: "http://localhost:8080" // Ruta a la API
}
```

En `nombremiEntidad/src/app` crear 3 folders:
- `components`
- `models`
- `services`

## Modules

Escribir en `mimiEntidad/src/app/app.module.ts`

##### app.module.ts
```typescript
// Default imports
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

// Handle HTTP mapping
import { HttpClientModule } from '@angular/common/http';

// Material
import { MatTableModule} from '@angular/material/table';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatButtonModule } from '@angular/material/button';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatMenuModule } from '@angular/material/menu';
import { MatToolbarModule } from '@angular/material/toolbar';

// Forms required
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    // Default
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,

    // Handle HTTP mapping
    HttpClientModule,

    // Material navigation
    MatMenuModule,
    MatToolbarModule,

    // Material table and pagination
    MatTableModule,
    MatPaginatorModule,

    // Material forms
    MatInputModule,
    MatFormFieldModule,
    MatSelectModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatButtonModule,

    // Forms required
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
```

## Models

En folder `models` crear un archivo `miEntidad.ts` por cada entitidad

##### miEntidad.ts
```typescript
export class MiEntidad {
  idMiEntidad:number=0;
  miAtributo:string=""; // Si es String
  miAtributo:number=0; // Si es Int o Double
  miAtributo:Date=new Date(Date.now()); // Si es Date
}
```
## Services

Por cada miEntidad.ts debemos ejecutar el siguiente comando en la consola
`ng g s services/miEntidad --skip-tests`

##### miEntidad.service.ts  
```typescript
import { MiEntidad } from '../models/miEntidad';
import { enviroment } from './../../../enviroments/enviroment';
import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { HttpClient } from '@angular/common/http';

const base_url = enviroment.base;

@Injectable({
    providedIn: 'root'
})
    export class MiEntidadService {
    private url = `${base_url}/miEntidad`
    private changesList = new Subject<MiEntidad[]>();

    constructor(private http:HttpClient) { }

    // API controller methods
    list(){
        return this.http.get<MiEntidad[]>(this.url);
    }

    insert(miEntidad:MiEntidad){
        return this.http.post(this.url,miEntidad);
    }

    // Changes list
    setList(newList:MiEntidad[]) {
        this.changesList.next(newList);
    }

    getList(){
        return this.changesList.asObservable();
    }
}
```

## Components

Por cada miEntidad.ts debemos ejecutar el siguiente comando en la consola: `ng g c components/miEntidad --skip-tests`

Por cada método de miEntidad.service.ts debemos ejecutar el siguiente comando en la consola: `ng g c components/miEntidad/miMetodo-miEntidad --skip-tests`. Usualmente usamos:

- `ng g c components/miEntidad/list-miEntidad --skip-tests`
- `ng g c components/miEntidad/insert-miEntidad --skip-tests`

### miEntidad component

##### miEntidad.component.ts
```typescript
import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-miEntidad',
  templateUrl: './miEntidad.component.html',
  styleUrls: ['./miEntidad.component.css']
})
export class MiEntidadComponent {
  constructor(public route: ActivatedRoute){}

  ngOnInit(): void {}
}
```

##### miEntidad.component.html
```html
<router-outlet></router-outlet>
<div [hidden]="route.children.length!==0">
  <app-list-miEntidad></app-list-miEntidad> <!-- Optional -->
</div>
```

### list-miEntidad component

##### list-miEntidad.component.ts
```typescript
import { Component, OnInit } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MiEntidad } from 'src/app/models/miEntidad';
import { MiEntidadService } from 'src/app/services/miEntidad.service';

@Component({
  selector: 'app-list-miEntidad',
  templateUrl: './list-miEntidad.component.html',
  styleUrls: ['./list-miEntidad.component.css']
})
export class ListMiEntidadComponent implements OnInit {
  dataSource: MatTableDataSource<MiEntidad> = new MatTableDataSource();
  displayedColumns: string[] = ['idMiEntidad', 'miAtributo', 'miAtributo'];
  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(private miEntidadService: MiEntidadService) {}

  ngOnInit(): void {
    this.miEntidadService.list().subscribe((data) => {
      this.dataSource = new MatTableDataSource(data);
      this.dataSource.paginator = this.paginator;
    });
  }
}
```

##### list-miEntidad.component.html
```html
<div class="mat-elevation-z8">

  <table mat-table [dataSource]="dataSource" class="mat-elevation-z8">

    <!-- id column -->
    <ng-container matColumnDef="idMiEntidad">
      <th mat-header-cell *matHeaderCellDef> idMiEntidad </th>
      <td mat-cell *matCellDef="let element"> {{element.idMiEntidad}} </td>
    </ng-container>

    <!-- attribute columns (just copy & paste) -->
    <ng-container matColumnDef="miAtributo">
      <th mat-header-cell *matHeaderCellDef> miAtributo </th>
      <td mat-cell *matCellDef="let element"> {{element.miAtributo}} </td>
    </ng-container>

    <ng-container matColumnDef="miAtributo">
      <th mat-header-cell *matHeaderCellDef> miAtributo </th>
      <td mat-cell *matCellDef="let element"> {{element.miAtributo}} </td>
    </ng-container>

    <ng-container matColumnDef="miAtributo">
      <th mat-header-cell *matHeaderCellDef> miAtributo </th>
      <td mat-cell *matCellDef="let element"> {{element.miAtributo | date:'dd/MM/yyyy'}} </td> <!-- Date format -->
    </ng-container>

    <!-- material definitions (no not touch)-->
    <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
    <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
  </table>

  <!-- material paginator (can be eliminated) -->
  <mat-paginator [pageSizeOptions]="[5, 10, 20]" showFirstLastButtons>
  </mat-paginator>

</div>
```

### insert-miEntidad component

##### insert-miEntidad.component.ts
```typescript

import { Component } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import * as moment from 'moment';
import { MiEntidad } from 'src/app/models/miEntidad';
import { MiEntidadService } from 'src/app/services/miEntidad.service';

@Component({
  selector: 'app-insert-miEntidad',
  templateUrl: './insert-miEntidad.component.html',
  styleUrls: ['./insert-miEntidad.component.css'],
})
export class InsertMiEntidadComponent {
  form: FormGroup = new FormGroup({});
  miEntidad: MiEntidad = new MiEntidad();
  message: string = '';

  // Conditional validation (not all attributes are required)
  maxMiAtributo: Date = moment().add(1, 'days').toDate(); // max date
  categoriesMiAtributo: { value: string; viewValue: string }[] = [
    { value: 'value1', viewValue: 'Value1' },
    { value: 'value2', viewValue: 'Value2' },
  ]; // select options

  constructor(
    private miEntidadService: MiEntidadService,
    private router: Router,
    private formBuilder: FormBuilder
  ) {}

  // Set validations except for ID attribute
  ngOnInit(): void {
    this.form = this.formBuilder.group({
      miAtributo: ['', Validators.required],
      miAtributo: ['', Validators.required]
    });
  }

  // Insert new record
  insert(): void {
    if (this.form.valid) {
      // Set values from form except for ID attribute
      this.miEntidad.miAtributo = this.form.value.miAtributo;
      this.miEntidad.miAtributo = this.form.value.miAtributo;
      
      console.log(this.miEntidad); // Debug in browser console

      this.miEntidadService.insert(this.miEntidad).subscribe(() => {
        this.miEntidadService.list().subscribe((data) => {
          this.miEntidadService.setList(data);
          this.router.navigate(['miEntidad/list']); // Go to list after insert
        });
      });
    } else {
      this.message = 'Missing filled values';
    }
  }

  getControlField(fieldName: string): AbstractControl {
    const control = this.form.get(fieldName);
    if (!control) {
      throw new Error(`Control not found for field {$fieldName}`)
    }
    return control;
  }
}
```

##### insert-miEntidad.component.html
```html
<div class="container col-6">
  <h1 class="text-center"> Insert </h1>
  <form [formGroup]="form" (submit)="insert()" class="row justify-content-center">

    <!-- For String / Integer attibute with free text -->
    <mat-form-field>
      <mat-label>MiAtributo</mat-label>
      <input matInput placeholder="place holder text" formControlName="miAtributo" />
      <mat-error *ngIf="getControlField('miAtributo')?.errors?.['required']" />
    </mat-form-field>

    <!-- For Date attribute -->
    <mat-form-field>
      <mat-label>MiAtributo</mat-label>
      <input matInput [matDatepicker]="picker" placeholder="place holder value" formControlName="miAtributo"
        [max]="maxMiAtributo" />
      <mat-hint>MM/DD/YYYY</mat-hint>
      <mat-datepicker-toggle matIconSuffix [for]="picker"></mat-datepicker-toggle>
      <mat-datepicker #picker></mat-datepicker>
      <mat-error *ngIf="getControlField('miAtributo')?.errors?.['required']" />
    </mat-form-field>

    <!-- For String / Integer attribute with options -->
    <mat-form-field>
      <mat-label>MiAtributo</mat-label>
      <mat-select formControlName="miAtributo">
        <mat-option *ngFor="let category of categoriesMiAtributo" [value]="category.value">
          {{ category.viewValue }}
        </mat-option>
      </mat-select>
      <mat-error *ngIf="getControlField('miAtributo')?.errors?.['required']" />
    </mat-form-field>

    <!-- Required Submit / Cancel buttons -->
    <button mat-raised-button color="primary">Submit</button>
    <button mat-button color="warn" routerLink="/miEntidad">Cancel</button>

  </form>
</div>
```

## Route HTML

##### app-routing.module.ts
```typescript
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MiEntidadComponent } from './components/miEntidad/miEntidad.component';
import { ListMiEntidadComponent } from './components/miEntidad/list-miEntidad/list-miEntidad.component';
import { InsertMiEntidadComponent } from './components/miEntidad/insert-miEntidad/insert-miEntidad.component';

const routes: Routes = [
  {
    path: 'miEntidad', component:MiEntidadComponent, children:[
      {
        path:'list', component:ListMiEntidadComponent
      },
      {
        path:'insert', component:InsertMiEntidadComponent
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
```

##### app.component.html
```html
<!-- Make up the navigation menu -->
<mat-toolbar color="primary">
  <button mat-button [matMenuTriggerFor]="menuMiEntidad">MiEntidad</button>
  <button mat-button [matMenuTriggerFor]="menuMiEntidad">MiEntidad</button>
</mat-toolbar>

<mat-menu #menuMiEntidad="matMenu">
  <button mat-menu-item routerLink="/miEntidad/list">list</button>
  <button mat-menu-item routerLink="/miEntidad/insert">insert</button>
</mat-menu>


<mat-menu #menuMiEntidad="matMenu">
  <button mat-menu-item routerLink="/miEntidad/list">list</button>
  <button mat-menu-item routerLink="/miEntidad/insert">insert</button>
</mat-menu>

<!-- Make up the content -->
<app-miEntidad></app-miEntidad>
<app-miEntidad></app-miEntidad>
```

##### miEntidad.component.html
```html
<router-outlet></router-outlet>
<div [hidden]="route.children.length!==0">
  <app-list-miEntidad></app-list-miEntidad> <!-- Optional -->
</div>
```
