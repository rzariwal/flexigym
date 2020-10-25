import { TestBed } from '@angular/core/testing';

import { AdvertiseService } from './advertise.service';

describe('AdvertiseService', () => {
  let service: AdvertiseService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AdvertiseService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
