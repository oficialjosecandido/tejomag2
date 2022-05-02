import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EstatutoEditorialComponent } from './estatuto-editorial.component';

describe('EstatutoEditorialComponent', () => {
  let component: EstatutoEditorialComponent;
  let fixture: ComponentFixture<EstatutoEditorialComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EstatutoEditorialComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EstatutoEditorialComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
