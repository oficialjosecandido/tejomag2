import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-dummy',
  templateUrl: './dummy.component.html',
  styleUrls: ['./dummy.component.css']
})
export class DummyComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
    this.hidePanels();
  }

  hidePanels() {
    let nav = document.getElementById('nav');
    let footer = document.getElementById('footer')
    if (nav != null) {
      nav.style.display = 'none';
    }
    if (footer != null) {
      footer.style.display = 'none';
    }
  }

}
