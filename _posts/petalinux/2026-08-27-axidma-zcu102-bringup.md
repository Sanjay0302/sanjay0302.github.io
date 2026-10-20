---
layout: post
title: AXIDMA Loopback Test - ZCU102
date: 2026-08-27 00:08 +0530
description: Using DMA in ZCU102 to exchange data from and to betwenn memory and IP block.
image:
  path: banner.gif
  lqip: data:image/webp;base64,UklGRpoAAABXRUJQVlA4WAoAAAAQAAAADwAABwAAQUxQSDIAAAARL0AmbZurmr57yyIiqE8oiG0bejIYEQTgqiDA9vqnsUSI6H+oAERp2HZ65qP/VIAWAFZQOCBCAAAA8AEAnQEqEAAIAAVAfCWkAALp8sF8rgRgAP7o9FDvMCkMde9PK7euH5M1m6VWoDXf2FkP3BqV0ZYbO6NA/VFIAAAA
category: [Linux, Xilinx, Petalinux, DMA]
tags: [petalinux, yocto, zcu102, mpsoc, fpga, dma]
author: sanjay0302
pin: false
math: true
mermaid: true
published: true
toc: true
comments: true
media_subpath: /_user_assets/petalinux/
---

In this post, we will walk through the bring-up and testing of the AXIDMA using vitis bare-metal examples and the petalinux axidmatest driver. The hardware configuration for this demonstration is based on the setup described at [fpgadeveloper.com](https://www.fpgadeveloper.com/2014/08/using-the-axi-dma-in-vivado.html), you can also refer the [youtube video](https://www.youtube.com/watch?v=Ld01yPmW_Xw); however, I have provided the full `.tcl` script for the vivado project to simplify the setup.

{% include embed/youtube.html id='Ld01yPmW_Xw' %}

> This project was developed using vivado 2022.2. To ensure compatibility, you must use the corresponding versions of petalinux and vitis.
{: .prompt-info }

```bash
# Open Vivado and use tcl console
# Navigate to home directory and verify path
cd [file normalize ~]
puts "Current working directory: [pwd]"

# Create and navigate to the working directory
file mkdir "[file normalize ~]/axidma-vivado"
cd "[file normalize ~]/axidma-vivado"
```

[axi-dma.tcl]: https://github.com/Sanjay0302/axidma-petalinux/blob/b35f0c39ab94c302b841f6f25c232c2ff58b5173/Hardware/zcu102-axi-hp.tcl

Downlaod this `.tcl` script [`axi-dma.tcl`][axi-dma.tcl] and save it inside `~/axidma-vivado`.

> This tcl script uses HP port, so this port doesn't suppport hardware cache coherency (cci-400).
>
> The script with `cci-400` will be explained in next blog.


```bash
# make sure to save the downloaded tcl script inside this folder ~/axidma-vivado
# source the .tcl file in vivado tcl console
# this also automatically opens the project folder ~/axidma-vivado/axi-dma
source "[file normalize ~]/axidma-vivado/axi-dma.tcl"
# Open the block design
open_bd_design "[file normalize ~]/axidma-vivado/axi-dma/axi-dma.srcs/sources_1/bd/design_1/design_1.bd"
# regenerate block design layout
regenerate_bd_layout
```

The block diagram would look similar to this;

![BD](axi-dma/dma-hp-bd.png){: .rounded lqip="{{ site.ph.lqip }}"}

```bash
# Run synthesis
launch_runs synth_1 -jobs 2
wait_on_run synth_1
# Run implementation
launch_runs impl_1 -jobs 2
wait_on_run impl_1
# Generate bitstream
launch_runs impl_1 -to_step write_bitstream -jobs 2
wait_on_run impl_1

# Export the Hardware Platform (XSA)
write_hw_platform -fixed -include_bit -force -file "[file normalize ~]/axidma-vivado/axi-dma/design_1_wrapper.xsa"

```

### ZCU102 Petalinux Build

> We need few pre-requisites for petalinux build to test the `axidma`, which includes downloading the offline files of petalinux `downloads`, `sstate-cache` for `aarch64` and petalinux toolchain.
> Follow the steps explained in [petalinux-starter-guide]({{ site.url }}/posts/petalinux-starter-guide).
{: .prompt-tip}

```bash
# open ubuntu bash terminal
cd $HOME
# Source petalinux tool chain
source $HOME/petalinux_downloads_sstate_shared/tools/petalinux/2022.2/settings.sh

# create zcu102 petalinux project
petalinux-create -t project --template zynqMP -n zcu102_axi_dma
cd zcu102_axi_dma

petalinux-config --get-hw-description=$HOME/axidma-vivado/axi-dma/design_1_wrapper.xsa
# this opens a blue menuconfig window and change the following config variables

```

| Configuration Option                    | Value                                                           | Description / Purpose                                        |
| --------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------ |
| `CONFIG_SUBSYSTEM_BOOTARGS_AUTO`        | `y`                                                             | Automatically generates kernel boot arguments                |
| `CONFIG_SUBSYSTEM_BOOTARGS_EARLYPRINTK` | `y`                                                             | Enables early printk in boot arguments                       |
| `CONFIG_SUBSYSTEM_EXTRA_BOOTARGS`       | `cma=1024M`                                                     | Appends custom extra arguments (e.g., CMA memory allocation) |
| `CONFIG_SUBSYSTEM_ROOTFS_EXT4`          | `y`                                                             | Configures the root filesystem type as EXT4                  |
| `SUBSYSTEM_SDROOT_DEV`                  | `/dev/sda1`                                                     | Specifies the SD/storage root device partition               |
| `CONFIG_SUBSYSTEM_HOSTNAME`             | `zcu102_axi_dma`                                                | Sets the target board hostname                               |
| `CONFIG_TMP_DIR_LOCATION`               | `${PROOT}/build/tmp`                                            | Defines the Yocto temporary build directory                  |
| `CONFIG_PRE_MIRROR_URL`                 | `file:///home/user/petalinux_downloads_sstate_shared/downloads` | Points to local source downloads mirror                      |
| `CONFIG_YOCTO_LOCAL_SSTATE_FEEDS_URL`   | `/home/user/petalinux_downloads_sstate_shared/aarch64`          | Specifies the local shared sstate feed path                  |
| `CONFIG_YOCTO_NETWORK_SSTATE_FEEDS`     | `n`                                                             | Disables network-based sstate feeds                          |
| `CONFIG_YOCTO_BB_NO_NETWORK`            | `y`                                                             | Forces offline BitBake builds without internet access        | **** |


After setting above configs, `CONFIG_SUBSYSTEM_USER_CMDLINE` will contain final kernel bootargs, which will look like `earlycon console=ttyPS0,115200 clk_ignore_unused root=/dev/sda1 rw rootwait cma=1024M`


---

### Kernel Configs

```bash
# set the kernel configuration options using 
petalinux-config -c kernel
```

| Kernel Configuration Option | Value  | Description / Purpose                                         |
| --------------------------- | ------ | ------------------------------------------------------------- |
| `CONFIG_DMATEST`            | `m`    | Enables the generic DMA test client as a loadable module      |
| `CONFIG_XILINX_ZYNQMP_DMA`  | `y`    | Enables the Xilinx ZynqMP DMA driver                          |
| `CONFIG_XILINX_DMATEST`     | `m`    | Enables the Xilinx DMA test client as a loadable module       |
| `CONFIG_XILINX_VDMATEST`    | `m`    | Enables the Xilinx Video DMA test client as a loadable module |
| `CONFIG_CMA_SIZE_MBYTES`    | `1024` | Sets the Contiguous Memory Allocator (CMA) size to 1024 MB    |
| `CONFIG_XILINX_DMA`         | `y`    | Enables the core Xilinx DMA engine driver                     |
| `CONFIG_ARM64_4K_PAGES`     | `4KB`  | Configures the ARM64 kernel page size to 4KB                  |
| `CONFIG_CMA`                | `y`    | Enables the Contiguous Memory Allocator subsystem             |
| `CONFIG_PARTITION_ADVANCED` | `y`    | Enables advanced partition table types support                |
| `CONFIG_EFI_PARTITION`      | `y`    | Enables GPT (EFI) partition table support                     |
| `CONFIG_USB_DWC3`           | `y`    | Enables DesignWare USB3 DRD controller driver                 |
| `CONFIG_USB_DWC3_DUAL_ROLE` | `y`    | Sets USB DWC3 controller to dual-role (Host/Device) mode      |
| `CONFIG_USB_SUPPORT`        | `y`    | Enables core USB support in the kernel                        |
| `CONFIG_USB_COMMON`         | `y`    | Enables common USB framework files                            |
| `CONFIG_USB_ARCH_HAS_HCD`   | `y`    | Indicates architecture has USB Host Controller Driver support |
| `CONFIG_USB`                | `y`    | Enables support for USB                                       |
| `CONFIG_USB_XHCI_HCD`       | `y`    | Enables xHCI USB controller support (USB 3.0)                 |
| `CONFIG_USB_XHCI_PLATFORM`  | `y`    | Enables generic platform xHCI controller driver               |


---

### Rootfs Configs

```bash
# set the rootfs configuration options 
petalinux-config -c rootfs
```

| RootFS Configuration Option / Recipe   | Value | Description / Purpose                                            |
| -------------------------------------- | ----- | ---------------------------------------------------------------- |
| `CONFIG_libmali-xlnx`                  | `y`   | Enables the Xilinx Mali GPU user-space library                   |
| `CONFIG_mali-backend-wayland`          | `y`   | Configures the Mali graphics backend for Wayland                 |
| `CONFIG_packagegroup-petalinux-weston` | `y`   | Includes the PetaLinux Weston (Wayland compositor) package group |
| `CONFIG_axidma-driver`                 | `y`   | Enables the custom AXI DMA driver recipe in the rootfs           |
| `CONFIG_auto-login`                    | `y`   | Enables automatic console login for the root user                |

---

### Device tree Overlay

```bash
# Build the device tree yocto task to updat the DTSI files
# This will get us system-user.dtsi and pl.dtsi
petalinux-build -c device-tree
```

Using this command the DMA IP block parameters are succesfully translated to devicetree node, it captures the memory mapped address, scatter gather settings, buffer length, read and write channel properties.

{% capture details_content %}
```c

/* file: ./components/plnx_workspace/device-tree/device-tree/pl.dtsi
 * CAUTION: This file is automatically generated by Xilinx.
 * Version: XSCT
 */

/ {
	amba_pl: amba_pl@0 {
		#address-cells = <2>;
		#size-cells = <2>;
		compatible = "simple-bus";
		ranges ;
		axi_dma_0: dma@a0000000 {
			#dma-cells = <1>;
			clock-names = "s_axi_lite_aclk", "m_axi_sg_aclk", "m_axi_mm2s_aclk", "m_axi_s2mm_aclk";
			clocks = <&zynqmp_clk 71>, <&zynqmp_clk 71>, <&zynqmp_clk 71>, <&zynqmp_clk 71>;
			compatible = "xlnx,axi-dma-7.1", "xlnx,axi-dma-1.00.a";
			interrupt-names = "mm2s_introut", "s2mm_introut";
			interrupt-parent = <&gic>;
			interrupts = <0 89 4 0 90 4>;
			reg = <0x0 0xa0000000 0x0 0x10000>;
			xlnx,addrwidth = <0x20>;
			xlnx,include-sg ;
			xlnx,sg-length-width = <0xe>;
			dma-channel@a0000000 {
				compatible = "xlnx,axi-dma-mm2s-channel";
				dma-channels = <0x1>;
				interrupts = <0 89 4>;
				xlnx,datawidth = <0x20>;
				xlnx,device-id = <0x0>;
			};
			dma-channel@a0000030 {
				compatible = "xlnx,axi-dma-s2mm-channel";
				dma-channels = <0x1>;
				interrupts = <0 90 4>;
				xlnx,datawidth = <0x20>;
				xlnx,device-id = <0x0>;
			};
		};
	};
};

```
{% endcapture %}
{% include details.html title="pl.dtsi" content=details_content %}

---

```bash
# edit the system-user.dtsi to enable usb host mode and axidmatest node
nano project-spec/meta-user/recipes-bsp/device-tree/files/system-user.dtsi
```

{% capture details_content %}

```c
/* the same overlay will be used by both kernel and uboot
 * file: project-spec/meta-user/recipes-bsp/device-tree/files/system-user.dtsi
*/

/include/ "system-conf.dtsi"
/ {

    // this node is needed to test axidma using axidmatest kernel module
    // this driver has to be manually probed by user
    // there is no modprobe.d rule for this official axidmatest driver from the kernel source
    dmatest_0: dmatest@0 {
        compatible = "xlnx,axi-dma-test-1.00.a";
        dmas = <&axi_dma_0 0 &axi_dma_0 1>;
        dma-names = "axidma0", "axidma1";
    };

    /* To use the changed PL clock in vivado zynq configuration menu,
     * specify that clock in DT to make the changes effective in the petalinux build.
     */
    fclk0 {
        status = "okay";
        assigned-clocks = <&zynqmp_clk PL0_REF>;
        assigned-clock-rates = <100000000>; // 100MHz
    };
};

/* Override the second channel's device-id to 1 so they are unique; 
 * Some driver expect the channel id to be unique.
 */
&axi_dma_0 {
    dma-channel@a0000030 {
        xlnx,device-id = <0x1>;
    };
};

// usb enable
&usb0 {
    status = "okay";
};

// usb as host mode to boot from flash drive
&dwc3_0 {
    status = "okay";
    dr_mode = "host";
};
```

{% endcapture %}
{% include details.html title="system-user.dtsi" content=details_content %}

---

### Build and Flash

Follow the same exact steps we discussed in
* [preparing-the-bootable-flash-drive]({{site.url}}/posts/petalinux-starter-guide/#preparing-the-bootable-flash-drive)
* [booting-bootloaders]({{site.url}}/posts/petalinux-starter-guide/#booting-bootloaders)

Once you are in u-boot hush shell, will boot kernel from usb flash drive manually

```bash
ext4ls usb 0:1 /boot/
ext4load usb 0:1 0x00200000 /boot/Image
ext4load usb 0:1 0x00100000 /boot/system.dtb
setenv bootargs "console=ttyPS0,115200 root=/dev/sda1 rw rootwait cma=1024M"
booti 0x00200000 - 0x00100000
```

Once booted will probe the axidmatest kernel module to verify the vivado hardware loopback design.

```bash
modprobe axidmatest

# will get following kernel logs which proves the successful integration of DMA and AXIS Data FIFO in loopback
# [  207.251636] dmatest: Started 1 threads using dma0chan0 dma0chan1
# [  207.273131] dma0chan0-dma0c: terminating after 5 tests, 0 failures 2162 iops 182958 KB/s (status 0)

#  you can also try multiple iterations also
modprobe axidmatest iterations=100

```
