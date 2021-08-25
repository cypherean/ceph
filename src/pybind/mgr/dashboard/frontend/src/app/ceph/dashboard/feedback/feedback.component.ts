import { Component } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';

import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

import { CdFormGroup } from '~/app/shared/forms/cd-form-group';
import { ActionLabelsI18n } from '~/app/shared/constants/app.constants';

import _ from 'lodash';

@Component({
  selector: 'cd-feedback',
  templateUrl: './feedback.component.html',
  styleUrls: ['./feedback.component.scss']
})
export class FeedbackComponent {
  title = 'Feedback';
  project: any = ['dashboard', 'block', 'objects', 'file_system', 'ceph_manager', 'orchestrator', 'ceph_volume', 'core_ceph'];
  tracker: any = ['bug', 'feature'];
  // severity: any = ['minor', 'major', 'critical']

  feedbackForm: CdFormGroup;
  constructor(
    public activeModal: NgbActiveModal,
    public actionLabels: ActionLabelsI18n
  ) {
    this.createForm();
  }

  private createForm() {
    this.feedbackForm = new CdFormGroup({
      project: new FormControl('', Validators.required),
      tracker: new FormControl('', Validators.required),
      subject: new FormControl('', Validators.required),
      description: new FormControl('', Validators.required),
    });
  }

  get f() {
    return this.feedbackForm.controls;
  }

  onSubmit() {
    fetch('/ui-api/feedback', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.ceph.api.v1.0+json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
      },
      body: JSON.stringify({ "project_id": this.feedbackForm.controls['project'].value, "tracker_id": this.feedbackForm.controls['tracker'].value, "subject": this.feedbackForm.controls['subject'].value, "description": this.feedbackForm.controls['description'].value })
    }).then((res) => {
      if (res.status != 201) {
        alert("Error:" + res.json())
      }
      return res.json()
    })
      .then((jsonData) => {
        if(jsonData['message'].length == 0) {
          alert("Key not set");
        }
        else {
          if (window.confirm('Issue successfully created: '+ jsonData['message'] + '. Click OK to open it in Ceph Issue Tracker and cancel to stay on this site.')) 
          {
            window.location.href='https://tracker.ceph.com/issues/'+jsonData['message'];
          };
          this.activeModal.close();
        }
      })
      .catch((err) => {
        // handle error
        alert(err);
        this.activeModal.close();
      });
  }
}
