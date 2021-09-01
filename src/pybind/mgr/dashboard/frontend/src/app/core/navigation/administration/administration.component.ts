import { Component } from '@angular/core';
import { NgbModalRef } from '@ng-bootstrap/ng-bootstrap';

import { Icons } from '~/app/shared/enum/icons.enum';
import { Permission } from '~/app/shared/models/permissions';
import { AuthStorageService } from '~/app/shared/services/auth-storage.service';
import { ModalService } from '~/app/shared/services/modal.service';
import { FeedbackComponent } from '~/app/ceph/shared/feedback/feedback.component';
@Component({
  selector: 'cd-administration',
  templateUrl: './administration.component.html',
  styleUrls: ['./administration.component.scss']
})
export class AdministrationComponent {
  userPermission: Permission;
  configOptPermission: Permission;
  icons = Icons;
  bsModalRef: NgbModalRef;

  constructor(private authStorageService: AuthStorageService, private modalService: ModalService) {
    const permissions = this.authStorageService.getPermissions();
    this.userPermission = permissions.user;
    this.configOptPermission = permissions.configOpt;
    
  }

  openFeedbackModal() {
    this.bsModalRef = this.modalService.show(FeedbackComponent);
  }
}
