<template>
	<div class="hello">
		<el-upload class="upload-demo"
		 action 
		:http-request="handleUpload" 
		:on-preview="handlePreview"
		:on-remove="handleRemove" 
		:on-success="handleSuccess" 
		:before-remove="beforeRemove"
		 multiple
		:file-list="fileList">
			<el-button size="small" type="primary">点击上传</el-button>
			<div slot="tip" class="el-upload__tip">{{ tip }}</div>
		</el-upload>

		<el-upload class="upload-demo" 
		drag 
		action 
		:http-request="handleUpload" 
		multiple
		:on-preview="handlePreview"
		:on-remove="handleRemove"
		:on-success="handleSuccess" 
		:before-remove="beforeRemove"
		:file-list="fileList"
		>
			<el-icon class="el-icon--upload"><upload-filled /></el-icon>
			<div class="el-upload__text">
				托转上传或 <em>点击上传</em>
			</div>
			<template #tip>
				<div class="el-upload__tip">
					上传列表
				</div>
			</template>
		</el-upload>
	</div>
</template>

<script>
	import {
		put,
		resumeUpload,
		signatureUrl,
		getFileNameUUID
	} from '../../store/ali-oss'
	import { mapState } from 'vuex'
	export default {
		name: 'Upload',
		props: {
			tip: {
				type: String,
				default: '上传大小不能超过80M'
			},
			limit: {
				type: Number,
				default: 1
			},
			action: {
				type: String,
				default: ''
			},
			headers: {
				type: Object,
				default: () => {}
			},
			name: {
				type: String,
				default: ''
			},
			listType: {
				type: String,
				default: 'text'
			}
		},
		computed: {
		  ...mapState({
			uploadList: state => state.upload.uploadData
		  })
		},
		data() {
			return {
				fileList: []
			}
		},
		methods: {
			handleRemove(file, fileList) {
				this.$emit('on-remove', file, fileList)
			},
			handlePreview(file) {
				this.$emit('on-preview', file)
			},
			handleExceed(files, fileList) {
				this.$message.warning(`每次只能上传 ${this.limit} 个文件`)
			},
			beforeRemove(file, fileList) {
				return this.$confirm(`确定移除 ${file.name}？`)
			},
			handleSuccess(response, file, fileList) {
				this.fileList = fileList
				this.$emit('on-success', file, fileList)
			},
			beforeUpload(file) {
				console.log(getFileName(file.name))
				// 限制上传类型      
				const fileExtensions = getFileName(file.name) === '.mp4' || getFileName(file.name) === '.docx' ||
					getFileName(file.name) === '.pdf'
				//限制的上限为20M      
				const max20M = file.size / 1024 / 1024 < 900;
				if (!fileExtensions) {
					this.$message.error('上传文件类型只能是 .doc, .docx, .pdf 格式!');
				}
				if (!max20M) {
					this.$message.error('上传文件大小不能超过 20MB!');
				}
				return fileExtensions && max20M;
			},
			/**
			 * 自定义上传方法
			 */
			handleUpload(option) {
				// 获取文件的后缀名
				var that = this;
				let objName = getFileNameUUID()
				var obj = option.file.name
				let OSS = require('ali-oss')
				
				let client = new OSS({
				  region: 'oss-cn-beijing',
				  secure: true,  // secure: 配合region使用，如果指定了secure为true，则使用HTTPS访问  
				  accessKeyId: 'LTAI5tF1BuAgVXZtax29gNzp',
				  accessKeySecret: 'h6zXOrNPwddoRIfxip2UqxmGl7r1fH',
				  bucket: 'awowyao'
				})
				
				
				objName = obj
				let checkpoint;
				const dataDic = {
				  fileUploadPercent: 0,
				  fileName: objName,
				  fileTime: '',
				  fileSpeed: ''
				}
				that.uploadList.push(dataDic)
				var ListIndex =  that.uploadList.length - 1
				for (let i = 0; i < 5; i++) {
				  try {
				    const result = client.multipartUpload(objName, option.file, {
				      checkpoint,
				      async progress(percentage, cpt) {
						that.uploadList[ListIndex].fileUploadPercent = Math.floor(percentage * 100)
						console.log(cpt)
				      },
				    });
				    break; // 跳出当前循环
					  
				  } catch (e) {
				    console.log(e);
				  }
				}
				
				// 调用 ali-oss 中的方法,flieName是存放的文件夹名称，可自己定义
				// resumeUpload(`flieName/${objName}`, option.file).then(res => {
				// 	console.log(res)
				// 	// 上传成功之后，转换真实的地址
				// 	signatureUrl(`flieName/${objName}`).then(res => {
				// 		console.log(res)
				// 	})
				// })
			}
		},
	}
</script>